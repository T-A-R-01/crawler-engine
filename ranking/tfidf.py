import math


def compute_tf(doc, query):
    words = doc.lower().split()
    return words.count(query.lower()) / len(words) if words else 0


def compute_idf(documents, query):
    count = 0
    for doc in documents:
        if query.lower() in doc.lower():
            count += 1

    if count == 0:
        return 0

    return math.log(len(documents) / count)