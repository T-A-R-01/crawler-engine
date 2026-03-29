import math


def compute_idf(documents, query_words):
    N = len(documents)
    idf = {}

    for word in query_words:
        count = 0
        for doc in documents:
            if word in doc.lower():
                count += 1

        idf[word] = math.log((N + 1) / (count + 1)) + 1

    return idf