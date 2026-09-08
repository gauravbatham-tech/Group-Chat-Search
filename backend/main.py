from typing import Optional

from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.search import search
from backend.ai import generate_answer
from backend.uploads import MAX_UPLOAD_BYTES, create_upload, get_upload, parse_chat_file
from backend.auth import authenticate, create_session, create_user, delete_session, get_user

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


class AuthRequest(BaseModel):
    name: str = ""
    email: str
    password: str


def current_user(authorization: str = Header(default="")):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Please sign in to continue.")
    user = get_user(authorization.removeprefix("Bearer ").strip())
    if not user:
        raise HTTPException(status_code=401, detail="Your session has expired. Please sign in again.")
    return user


@app.get("/")
def home():
    return {"message": "ChatSense API is running"}


@app.post("/auth/signup")
def signup(request: AuthRequest):
    if len(request.name.strip()) < 2:
        raise HTTPException(status_code=400, detail="Please enter your name.")
    if len(request.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")
    user = create_user(request.name, request.email, request.password)
    if not user:
        raise HTTPException(status_code=409, detail="An account with that email already exists.")
    return {"token": create_session(user), "user": {"name": user["name"], "email": user["email"]}}


@app.post("/auth/login")
def login(request: AuthRequest):
    user = authenticate(request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Email or password is incorrect.")
    return {"token": create_session(user), "user": {"name": user["name"], "email": user["email"]}}


@app.get("/auth/me")
def me(user=Depends(current_user)):
    return {"name": user["name"], "email": user["email"]}


@app.post("/auth/logout")
def logout(authorization: str = Header(default="")):
    if authorization.startswith("Bearer "):
        delete_session(authorization.removeprefix("Bearer ").strip())
    return {"message": "Signed out"}


@app.post("/upload")
async def upload_chat(file: UploadFile = File(...), user=Depends(current_user)):
    if not file.filename or not file.filename.lower().endswith((".txt", ".json")):
        raise HTTPException(status_code=400, detail="Upload a WhatsApp .txt export or a messages .json file.")

    content = await file.read()
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="That file is too large. Please upload a file under 10 MB.")

    try:
        messages = parse_chat_file(file.filename, content)
        chat_id = create_upload(messages, user["id"])
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return {
        "chat_id": chat_id,
        "message_count": len(messages),
        "participant_count": len({message["sender"] for message in messages}),
    }


@app.post("/search")
def perform_search(request: SearchRequest, chat_id: Optional[str] = None, user=Depends(current_user)):
    source_messages = None
    source_embeddings = None
    if chat_id:
        upload = get_upload(chat_id, user["id"])
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