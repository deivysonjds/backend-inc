import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

class Postegre:


    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv('HOST_DB'),
            database=os.getenv('DATABASE_NAME'),
            user=os.getenv('USER_DB'),
            password=os.getenv('PASSWORD_DB')
        )

        self.cursor = self.conn.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id SERIAL PRIMARY KEY,
            url TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()
        pass        
    
    def save_url(self, url):
        try:
            self.cursor.execute(
                "INSERT INTO urls (url) VALUES (%s)",
                (url,)
            )
            self.conn.commit()
            return True
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            return False
            

postegre = Postegre()