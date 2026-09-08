from sentence_transformers import SentenceTransformer
import numpy as np
import json

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("data/messages.json", "r", encoding="utf-8") as f:
    messages = json.load(f)

texts = [m["message"] for m in messages]

embeddings = model.encode(
    texts,
    show_progress_bar=True,
    normalize_embeddings=True
)

np.save("data/embeddings.npy", embeddings)

print("Saved:", embeddings.shape)