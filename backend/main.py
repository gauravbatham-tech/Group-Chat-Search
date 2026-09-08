from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.search import search
from backend.ai import generate_answer

app = FastAPI(title="ChatSense")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


@app.get("/")
def home():
    return {"message": "ChatSense API is running"}


@app.post("/search")
def perform_search(request: SearchRequest):

    results = search(
        request.query,
        request.top_k
    )

    answer = generate_answer(
        request.query,
        results
    )

    return {
        "query": request.query,
        "answer": answer,
        "results": results
    }