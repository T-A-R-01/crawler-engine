from fastapi import FastAPI, Query
from database.db import Database
from ranking.tfidf import compute_idf, compute_tf

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Mini Search Engine API is running 🚀"}


@app.get("/search")
def search(q: str = Query(..., min_length=1)):
    db = Database()
    conn = db.conn
    cursor = conn.cursor()

    # Fetch data
    cursor.execute("SELECT url, title, content FROM pages")
    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return []

    documents = [row[2] for row in rows]

    # Compute IDF
    idf = compute_idf(documents, q)

    results = []

    max_score = 0

    # Compute scores
    for (url, title, content) in rows:
        tf = compute_tf(content, q)
        score = tf * idf

        if score > max_score:
            max_score = score

        results.append({
            "url": url,
            "title": title,
            "content": content,
            "raw_score": score
        })

    # Normalize scores + add snippet
    final_results = []
    for r in results:
        normalized_score = r["raw_score"] / max_score if max_score > 0 else 0

        final_results.append({
            "url": r["url"],
            "title": r["title"],
            "score": round(normalized_score, 4),
            "snippet": r["content"][:200] if r["content"] else ""
        })

    # Sort by score
    final_results.sort(key=lambda x: x["score"], reverse=True)

    return final_results[:10]