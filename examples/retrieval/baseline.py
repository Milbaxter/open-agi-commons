"""Frozen teaching baseline: count raw query substrings, including repeated matches."""


def rank(query, documents):
    terms = query.casefold().split()
    scores = [(sum(doc["text"].casefold().count(term) for term in terms), doc["id"])
              for doc in documents]
    return [doc_id for score, doc_id in sorted(scores, key=lambda item: (-item[0], item[1]))
            if score > 0]
