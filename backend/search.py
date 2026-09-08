from sentence_transformers import SentenceTransformer
import numpy as np
import json
import re
from datetime import datetime, timedelta

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

with open("data/messages.json", "r", encoding="utf-8") as f:
    messages = json.load(f)

embeddings = np.load("data/embeddings.npy")

PEOPLE = [
    "Rahul", "Priya", "Aman", "Neha",
    "Rohit", "Anjali", "Karan", "Sneha"
]

STOPWORDS = {
    "what", "when", "where", "who", "why", "how",
    "did", "do", "we", "the", "a", "an", "is",
    "was", "were", "on", "in", "to", "of", "for",
    "about", "our", "they", "their", "and"
}


def words(text):
    return set(
        w for w in re.findall(r"\b\w+\b", text.lower())
        if w not in STOPWORDS
    )


def get_date_filter(query):

    today = datetime(2026, 9, 7)
    q = query.lower()

    if "last month" in q:
        end = today.replace(day=1) - timedelta(days=1)
        start = end.replace(day=1)
        return start, end

    if "this month" in q:
        return today.replace(day=1), today

    if "last week" in q:
        return today - timedelta(days=7), today

    return None, None


def search(query, top_k=5, context=2, source_messages=None, source_embeddings=None):

    search_messages = source_messages if source_messages is not None else messages
    search_embeddings = source_embeddings if source_embeddings is not None else embeddings

    q = query.lower()

    people = sorted({message["sender"] for message in search_messages})
    person = next(
        (name for name in people if name.lower() in q),
        None
    )

    start_date, end_date = get_date_filter(query)

    query_words = words(query)

    # Candidate filtering
    candidates = []

    for i, message in enumerate(search_messages):

        if person and message["sender"] != person:
            continue

        date = datetime.fromisoformat(message["timestamp"])

        if start_date and not (start_date <= date <= end_date):
            continue

        candidates.append(i)

    # Semantic similarity
    query_embedding = MODEL.encode(
        [query],
        normalize_embeddings=True
    )[0]

    semantic_scores = search_embeddings @ query_embedding

    ranked_scores = []

    for i in candidates:

        message_words = words(search_messages[i]["message"])

        if query_words:
            keyword_score = len(
                query_words & message_words
            ) / len(query_words)
        else:
            keyword_score = 0

        # Hybrid score
        final_score = (
            0.75 * float(semantic_scores[i])
            + 0.25 * keyword_score
        )

        ranked_scores.append(
            (i, final_score)
        )

    ranked_scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    results = []

    for index, score in ranked_scores[:top_k]:

        start = max(0, index - context)
        end = min(len(search_messages), index + context + 1)

        results.append({
            "message": search_messages[index],
            "score": round(score, 4),
            "context": search_messages[start:end]
        })

    return results