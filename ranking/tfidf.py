import math
import re


def tokenize(text):
    # remove punctuation + lowercase
    return re.findall(r'\b[a-z]+\b', text.lower())


def compute_tf(doc, query):
    doc_words = tokenize(doc)
    query_words = tokenize(query)

    if not doc_words:
        return 0

    tf = 0
    for q in query_words:
        tf += doc_words.count(q) / len(doc_words)

    return tf


def compute_idf(documents, query):
    N = len(documents)
    query_words = tokenize(query)

    idf = {}

    for q in query_words:
        count = sum(1 for doc in documents if q in tokenize(doc))
        idf[q] = math.log((N + 1) / (count + 1)) + 1  # smooth IDF

    return idf


def compute_score(doc, query, idf):
    doc_words = tokenize(doc)
    query_words = tokenize(query)

    if not doc_words:
        return 0

    score = 0

    for q in query_words:
        tf = doc_words.count(q) / len(doc_words)
        score += tf * idf.get(q, 0)

    # 🔥 Boost score if query word exists
    if any(q in doc_words for q in query_words):
        score *= 5

    return score