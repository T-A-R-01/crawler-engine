from fastapi import APIRouter, Query
from database.db import Database
from ranking.tfidf import compute_idf

router = APIRouter()


def compute_score(content, query_words, idf):
    words = content.lower().split()
    score = 0

    for word in query_words:
        tf = words.count(word) / (len(words) + 1)
        score += tf * idf.get(word, 0)

    return score


def generate_snippet(content, query):
    content_lower = content.lower()
    query_lower = query.lower()

    idx = content_lower.find(query_lower)

    if idx != -1:
        start = max(0, idx - 100)
        end = min(len(content), idx + 100)
        return content[start:end]

    return content[:200]


@router.get("/search")
def search(q: str = Query(..., min_length=1)):
    db = Database()
    conn = db.conn
    cursor = conn.cursor()

    # Fetch all pages
    cursor.execute("SELECT url, title, content FROM pages")
    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return {"results": [], "count": 0}

    # Split query into words
    query_words = q.lower().split()

    # Prepare documents
    documents = [row[2] for row in rows]

    # Compute IDF
    idf = compute_idf(documents, query_words)

    results = []

    for row in rows:
        url, title, content = row

        # Base TF-IDF score
        score = compute_score(content, query_words, idf)

        # Boost if words appear in title
        for word in query_words:
            if word in title.lower():
                score *= 2

        # Boost if words appear early in content
        words = content.lower().split()
        for word in query_words:
            if word in words[:50]:
                score *= 1.5

        # Exact match boost
        for word in query_words:
            if word in content.lower():
                score *= 1.1

        if score > 0:
            results.append({
                "url": url,
                "title": title,
                "score": score,
                "snippet": generate_snippet(content, q)
            })

    # Sort results
    results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "results": results[:10],
        "count": len(results)
    }