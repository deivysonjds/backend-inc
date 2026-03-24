from fastapi import FastAPI
from model.model_manager import model_manager
from scraping.search_page import scraping
from db.pinecone_manager import pc
from db.postegres_connection import postegre
from fastapi.middleware.cors import CORSMiddleware

import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
    os.getenv('URL_CLIENT_DEPLOY')
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # quem pode acessar
    allow_credentials=True,
    allow_methods=["*"],    # GET, POST, PUT, DELETE...
    allow_headers=["*"],    # headers permitidos
)

@app.post("/scrape")
async def scrape(url: str):
    if not postegre.save_url(url):
        return {"message": f"Not saved url's {url}"}

    html = await scraping.scrap_page(url)
    text = scraping.extract_text(html)
    chunks = model_manager.chunk_text(text)
    embeddings = model_manager.generate_embeddings(chunks)

    pc.upsert_chunks(chunks, embeddings, url)
    return {"message": f"Saved url -> {url}"}


@app.post("/search")
async def search(query: str):
    embedding_query = model_manager.embed_query(query)
    response = pc.search(embedding_query)
    return {"result": response}

@app.get("/")
async def home():
    return {"message": "Server is running"}