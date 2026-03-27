import psycopg2
import os

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS pages (
            id SERIAL PRIMARY KEY,
            url TEXT UNIQUE,
            title TEXT,
            content TEXT
        );
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()

    def insert_page(self, url, title, content):
        try:
            cursor = self.conn.cursor()

            query = """
            INSERT INTO pages (url, title, content)
            VALUES (%s, %s, %s)
            ON CONFLICT (url) DO NOTHING;
            """

            cursor.execute(query, (url, title, content))
            self.conn.commit()
            cursor.close()

        except Exception as e:
            print("DB Error:", e)

    def close(self):
        self.conn.close()