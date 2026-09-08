# ChatSense

Semantic search engine for group chat conversations.

ChatSense allows users to search a large group-chat dataset using natural-language queries instead of exact keywords.

## Features

* Semantic search using sentence embeddings
* Hybrid semantic + keyword retrieval
* Search by person
* Temporal filtering
* Conversation context around matching messages
* AI-generated answers using Gemini
* Hinglish / code-mixed conversation support
* SQLite message storage
* FastAPI backend
* Simple HTML/CSS/JavaScript frontend

## Project Structure

```text
Group-Chat-Search/
│
├── backend/
│   ├── main.py
│   ├── search.py
│   ├── database.py
│   ├── models.py
│   ├── generate_data.py
│   ├── create_embeddings.py
│   └── ai.py
│
├── data/
│   ├── messages.json
│   ├── chat.db
│   └── embeddings.npy
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── tests/
│   ├── queries.json
│   └── evaluate.py
│
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

## Tech Stack

* Python
* FastAPI
* Sentence Transformers
* FAISS / vector search
* NumPy
* SQLite
* Google Gemini API
* HTML
* CSS
* JavaScript

## How It Works

```text
User Query
    ↓
FastAPI Backend
    ↓
Query Embedding
    ↓
Semantic Similarity Search
    ↓
Keyword + Metadata Filtering
    ↓
Top Matching Messages
    ↓
Conversation Context
    ↓
Gemini
    ↓
Answer + Sources
```

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Group-Chat-Search
```

### 2. Create virtual environment

```bash
python -m venv venv
```

Activate it on Git Bash:

```bash
source venv/Scripts/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY_HERE
```

Never commit `.env` or expose your API key.

### 5. Generate the dataset

```bash
python backend/generate_data.py
```

### 6. Create the database

```bash
python backend/database.py
```

### 7. Generate embeddings

```bash
python backend/create_embeddings.py
```

### 8. Start the backend

```bash
uvicorn backend.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

### 9. Open the frontend

Open:

```text
frontend/index.html
```

directly in your browser.

## Example Queries

```text
When did we decide on the trip?

What did Priya say about the budget?

What did we discuss last month?

Which destination did the group finally choose?

What did Aman suggest?

Who volunteered to check the tickets?
```

## Testing

Run:

```bash
python tests/evaluate.py
```

The evaluator checks whether the expected answer message appears in the top-5 retrieved results.

## Important Notes

* The dataset is synthetic.
* The Gemini API key must remain private.
* The virtual environment must not be committed to Git.
* Embeddings must be regenerated whenever the dataset changes.
