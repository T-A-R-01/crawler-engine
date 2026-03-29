import psycopg2
import os

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv("DATABASE_URL"))

    def close(self):
        self.conn.close()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pages (
                id SERIAL PRIMARY KEY,
                url TEXT UNIQUE,
                title TEXT,
                content TEXT
            )
        """)
        self.conn.commit()

    def insert_page(self, url, title, content):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO pages (url, title, content)
                VALUES (%s, %s, %s)
                ON CONFLICT (url) DO NOTHING
            """, (url, title, content))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("DB Error:", e)

    def close(self):
        self.conn.close()