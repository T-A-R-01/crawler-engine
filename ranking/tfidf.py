import math
import re

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

def compute_tf(doc, query):
    words = tokenize(doc)
    query_words = tokenize(query)

    tf = 0
    for q in query_words:
        tf += words.count(q)

    return tf / len(words) if len(words) > 0 else 0


def compute_idf(documents, query):
    query_words = tokenize(query)
    N = len(documents)

    idf = 0
    for q in query_words:
        containing_docs = sum(1 for doc in documents if q in tokenize(doc))
        if containing_docs > 0:
            idf += math.log(N / containing_docs)

    return idf