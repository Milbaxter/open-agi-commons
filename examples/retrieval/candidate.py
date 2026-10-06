"""Teaching candidate: match whole words and prefer coverage of distinct query terms."""

import re


def words(text):
    return set(re.findall(r"[a-z0-9]+", text.casefold()))


def rank(query, documents):
    terms = words(query)
    scores = [(len(terms & words(doc["text"])), doc["id"]) for doc in documents]
    return [doc_id for score, doc_id in sorted(scores, key=lambda item: (-item[0], item[1]))
            if score > 0]
