from fastapi import FastAPI, Query
from database.db import Database
from ranking.tfidf import compute_idf, compute_score

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Search API is running "}


@app.get("/search")
def search(q: str = Query(..., min_length=1)):
    try:
        db = Database()
        conn = db.conn
        cursor = conn.cursor()

        # Fetch all pages
        cursor.execute("SELECT url, title, content FROM pages")
        rows = cursor.fetchall()

        cursor.close()
        db.close()

        if not rows:
            return {"results": [], "count": 0}

        # Extract documents
        documents = [row[2] for row in rows]

        # Compute IDF
        idf = compute_idf(documents, q)

        results = []

        for row in rows:
            url, title, content = row

            score = compute_score(content, q, idf)

            results.append({
                "url": url,
                "title": title,
                "score": score,
                "snippet": content[:200]
            })

        # Sort by score (descending)
        results = sorted(results, key=lambda x: x["score"], reverse=True)

        return {
            "results": results[:20],  # limit results
            "count": len(results)
        }

    except Exception as e:
        return {
            "error": str(e)
        }