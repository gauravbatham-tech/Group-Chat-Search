# 💬 ChatSense — Semantic Group Chat Search

> Search conversations by **meaning, person, and time** — not just keywords.

ChatSense is an AI-powered semantic search engine built for large group-chat conversations.

Instead of requiring users to remember the exact words used in a conversation, ChatSense understands the **meaning of a query** and retrieves the most relevant messages along with their surrounding conversation context.

## 🚀 Demo Queries

Try queries like:

* **"When did we decide on the trip?"**
* **"What did Priya say about the budget?"**
* **"What did we discuss last month?"**
* **"Which destination did the group finally choose?"**

The system retrieves the relevant conversation and uses Gemini to generate a concise answer based only on the retrieved messages.

## ✨ Features

| Feature              | Description                                        |
| -------------------- | -------------------------------------------------- |
| 🧠 Semantic Search   | Finds messages based on meaning                    |
| 🔎 Hybrid Retrieval  | Combines semantic similarity with keyword matching |
| 👤 Person Search     | Filter conversations by participant                |
| 📅 Temporal Search   | Supports queries such as "last month"              |
| 💬 Context Retrieval | Shows surrounding conversation                     |
| 🤖 AI Answers        | Generates answers using Gemini                     |
| 🌐 Hinglish Support  | Handles code-mixed conversations                   |
| ⚡ Fast API           | FastAPI-powered backend                            |

## 🏗️ Architecture

```text
                    ┌─────────────────┐
                    │     User        │
                    │     Query       │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │    FastAPI      │
                    │    Backend      │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Query Embedding │
                    └────────┬────────┘
                             ↓
              ┌────────────────────────────┐
              │ Hybrid Retrieval           │
              │                            │
              │ Semantic Similarity        │
              │ + Keyword Matching         │
              │ + Person/Date Filtering    │
              └─────────────┬──────────────┘
                            ↓
                    ┌─────────────────┐
                    │ Top Messages +  │
                    │ Context         │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │     Gemini      │
                    │  Answer Engine  │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Answer + Sources│
                    └─────────────────┘
```

## 🛠️ Tech Stack

**Backend**

* Python
* FastAPI
* Sentence Transformers
* NumPy
* SQLite

**AI**

* Google Gemini
* Sentence embeddings

**Frontend**

* HTML
* CSS
* JavaScript

**Testing**

* Python
* Custom retrieval evaluation

## 📁 Project Structure

```text
Group-Chat-Search/
│
├── backend/          # API, search, AI and data processing
├── data/             # Chat dataset, database and embeddings
├── frontend/         # Web interface
├── tests/            # Retrieval evaluation
├── requirements.txt
└── README.md
```

## ⚙️ Running Locally

### Clone

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Group-Chat-Search
```

### Install

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

### Environment Variable

Create `.env`:

```env
GEMINI_API_KEY=YOUR_API_KEY_HERE
```

### Start

```bash
uvicorn backend.main:app --reload
```

Then open:

```text
frontend/index.html
```

## 🧪 Evaluation

The project includes a 40-query evaluation set for measuring retrieval performance.

Run:

```bash
python tests/evaluate.py
```

The evaluator reports **Top-5 Retrieval Accuracy**.

## 🎯 Problem Solved

Traditional chat search depends heavily on exact keywords.

For example, a user may ask:

> "When did we decide on the trip?"

while the actual message might say:

> "Okay guys, Manali it is. Let's book it."

A keyword search can miss this completely.

ChatSense uses semantic embeddings to connect the **intent of the query** with the **meaning of the message**.

## 🔐 Security

API keys and local virtual environments are excluded using `.gitignore`.

Never commit:

```text
.env
venv/
```

## 📌 Project Status

🚧 **In Development**

Core semantic search, metadata filtering, conversation context retrieval, AI answering, synthetic dataset generation, and evaluation infrastructure are implemented.

## 👨‍💻 Author

**Gaurav Batham**

Built as a practical AI/search engineering project demonstrating semantic retrieval, hybrid search, backend API development, and LLM-based question answering.

