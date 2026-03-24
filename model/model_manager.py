from openai import OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

import os
from dotenv import load_dotenv
load_dotenv()

class ModelManager:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def chunk_text(self, texts):
        if isinstance(texts, str):
            texts = [texts]
            
        chunks = []
        for text in texts:
            chunks.extend(self.splitter.split_text(text))

        return chunks

    def generate_embeddings(self, chunks: list) -> list:
        response = self.client.embeddings.create(
            input=chunks,
            model="text-embedding-3-small"
        )
        
        return [item.embedding for item in response.data]

    def embed_query(self, query):
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=[query]
        )
        
        return response.data[0].embedding


model_manager = ModelManager()