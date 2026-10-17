# FastAPI RAG Practice Project

A basic Retrieval-Augmented Generation (RAG) learning project built with FastAPI, LangChain, Qdrant, and Ollama.

## What It Does

1. **Loads & Chunks PDF:** Reads the document (`aiayn.pdf`) from the `data/` directory and splits it into smaller text chunks using LangChain.
2. **Generates Embeddings:** Converts the text chunks into vector embeddings using HuggingFace's `all-MiniLM-L6-v2` model.
3. **Stores Vectors:** Saves vector embeddings in a Qdrant collection running inside a Docker container.
4. **Queries & Responds:** Accepts user questions via a POST endpoint (`/query`), retrieves relevant PDF context chunks, and generates an answer using a local Ollama `llama3.2` model.

## Stack

* **API Framework**: FastAPI
* **LLM**: Ollama (`llama3.2`)
* **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
* **Vector Database**: Qdrant (via Docker)
* **PDF Loader & Chunker**: LangChain (`PyMuPDFLoader`, `RecursiveCharacterTextSplitter`)

## Requirements

* Python 3.10+
* Docker Desktop
* Ollama running locally with `llama3.2` downloaded (`ollama pull llama3.2`)

## How to Run

### 1. Set up virtual environment & dependencies

```bash
python -m venv venv
venv\Scripts\Activate
pip install -r requirements.txt
```

### 2. Start Qdrant via Docker

```bash
docker run -d -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### 3. Embed the PDF data

Run the indexing script to parse the PDF in `app/data/aiayn.pdf` and insert embeddings into Qdrant:

```bash
python index.py
```

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` in your browser to test the `/query` endpoint.

## Author

 **Ayushi Singh** 
 **GitHub Profile:** https://github.com/ayus28ayushi-ai