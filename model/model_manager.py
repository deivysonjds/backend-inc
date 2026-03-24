from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

class ModelManager:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", " ", ""]
        )
    
    def __init__(self):
        pass

    def chunk_text(self, texts):
        if isinstance(texts, str):
            texts = [texts]
            
        chunks = []
        for text in texts:
            chunks.extend(self.splitter.split_text(text))

        return chunks

    def generate_embeddings(self, chunks: list) -> list:
        return self.model.encode(chunks).tolist()

    def embed_query(self, query):
        return self.model.encode([query]).tolist()[0]

model_manager = ModelManager()