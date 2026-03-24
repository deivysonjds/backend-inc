import os
from dotenv import load_dotenv
from pinecone import Pinecone
load_dotenv()

class PineconeManager:
    pc = Pinecone(
        api_key=os.getenv("PINECONE_API_KEY"),
        environment=os.getenv("PINECONE_ENV")
    )

    INDEX_NAME = os.getenv("INDEX_NAME")
    def __init__(self):
        if self.INDEX_NAME not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.INDEX_NAME,
                dimension=384
            )
        self.index = self.pc.Index(self.INDEX_NAME)
        pass
        
    def upsert_chunks(self, chunks, embeddings, url):

        data = []

        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            data.append((
                f"{hash(url)}_{i}",  # ID único
                emb,
                {
                    "text": chunk,
                    "source": url
                }
            ))

        self.index.upsert(data)

    def search(self, query_embedding, top_k=3):

        result = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
            )

        return [
            {
                "text": match["metadata"]["text"],
                "score": match["score"],
                "source": match["metadata"]["source"]
            }
            for match in result["matches"]
        ]

pc = PineconeManager()
