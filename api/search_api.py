from fastapi import FastAPI, Query
import sqlite3
from collections import Counter
import math


app = FastAPI()


# -------------------------------
# DATABASE CONNECTION
# -------------------------------


def get_db_connection():
    return psycopg2.connect(
        dbname="crawler_db",
        user="postgres",
        password="YOUR_PASSWORD",
        host="localhost",
        port="5432"
    )


# -------------------------------
# HOME ROUTE
# -------------------------------
@app.get("/")
def home():
    return {"message": "Search API is running"}


# -------------------------------
# TF (Term Frequency)
# -------------------------------
def compute_tf(text, query):
    words = text.lower().split()
    word_count = Counter(words)
    total_words = len(words)

    if total_words == 0:
        return 0

    return word_count[query.lower()] / total_words


# -------------------------------
# IDF (Inverse Document Frequency)
# -------------------------------
def compute_idf(documents, query):
    num_docs = len(documents)
    count = sum(1 for doc in documents if query.lower() in doc.lower())

    return math.log((num_docs + 1) / (count + 1)) + 1


# -------------------------------
# SEARCH API WITH RANKING
# -------------------------------
@app.get("/search")
def search(q: str = Query(..., min_length=1)):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all pages
    cursor.execute("SELECT url, title, content FROM pages")
    rows = cursor.fetchall()

    conn.close()

    documents = [row[2] for row in rows]

    # Compute IDF once for query
    idf = compute_idf(documents, q)

    results = []

    for url, title, content in rows:
        tf = compute_tf(content, q)
        score = tf * idf

        if score > 0:
            results.append({
                "url": url,
                "title": title,
                "score": round(score, 5)
            })

    # Sort by relevance (highest score first)
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    # Return top 10 results
    return results[:10]