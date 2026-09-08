from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.search import search
from backend.ai import generate_answer
from backend.uploads import MAX_UPLOAD_BYTES, create_upload, get_upload, parse_chat_file

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


@app.post("/upload")
async def upload_chat(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith((".txt", ".json")):
        raise HTTPException(status_code=400, detail="Upload a WhatsApp .txt export or a messages .json file.")

    content = await file.read()
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="That file is too large. Please upload a file under 10 MB.")

    try:
        messages = parse_chat_file(file.filename, content)
        chat_id = create_upload(messages)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return {
        "chat_id": chat_id,
        "message_count": len(messages),
        "participant_count": len({message["sender"] for message in messages}),
    }


@app.post("/search")
def perform_search(request: SearchRequest, chat_id: Optional[str] = None):
    source_messages = None
    source_embeddings = None
    if chat_id:
        upload = get_upload(chat_id)
        if upload is None:
            raise HTTPException(status_code=404, detail="This uploaded archive has expired or does not exist.")
        source_messages = upload["messages"]
        source_embeddings = upload["embeddings"]

    results = search(
        request.query, request.top_k,
        source_messages=source_messages,
        source_embeddings=source_embeddings,
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