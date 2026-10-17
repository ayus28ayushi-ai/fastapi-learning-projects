# Contract Analysis API

A simple FastAPI backend built as a learning project to upload contract documents, parse their text content, perform AI analysis using **Google Gemini AI**, and store both contract metadata and analysis results in **MongoDB**.

## Tech Stack

* **Framework:** FastAPI
* **Database:** MongoDB (via PyMongo)
* **AI Integration:** Google GenAI SDK (`google-genai`)
* **Data Validation:** Pydantic v2
* **Containerization:** Docker & Docker Compose

## Project Structure

```text
ContractAnalysisAPI/
│
├── app/
│   ├── routes/
│   │   ├── analysis.py            
│   │   └── contracts.py           
│   ├── service/
│   │   ├── analyse_contract.py     
│   │   ├── document_parser.py     
│   │   └── prompt.py              
│   ├── config.py                  
│   ├── database.py                
│   ├── main.py                    
│   └── models.py                  
│
├── uploads/                       
├── .env                           
├── .gitignore
├── docker-compose.yml             
├── project_flow.md                
├── readme.md                      
└── requirements.txt               
```

## Features

* **Contract Management:** Upload contract files, store uploaded files locally, parse text content, and fetch metadata.
* **AI Analysis:** Send parsed contract text to Google Gemini to extract summaries, key clauses, and risk factors.
* **MongoDB Storage:** Persists uploaded contracts and analysis results in separate MongoDB collections.

## Getting Started

### Prerequisites

* Python 3.10+
* Docker & Docker Compose
* Google Gemini API Key

### 1. Environment Setup

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
MONGODB_URI=mongodb://admin:password@localhost:27017/
```

### 2. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run MongoDB with Docker

Start MongoDB using Docker Compose:

```bash
docker compose up -d
```

### 4. Run the Server

Start the application with Uvicorn:

```bash
uvicorn app.main:app --reload
```

Interactive API documentation will be available at `http://127.0.0.1:8000/docs`.

## API Endpoints

### Default

| Method | Endpoint | Description |
| ----- | ----- | ----- |
| `GET` | `/` | Root health check |

### Contracts

| Method | Endpoint | Description |
| ----- | ----- | ----- |
| `POST` | `/contracts/upload` | Upload contract document file |
| `GET` | `/contracts/` | List all uploaded contracts |
| `GET` | `/contracts/{id}` | Get specific contract by ID |

### Analysis

| Method | Endpoint | Description |
| ----- | ----- | ----- |
| `POST` | `/analysis/analyse/{contract_id}` | Perform Gemini analysis on a contract by ID |
| `GET` | `/analysis/{analysis_id}` | Get specific analysis result by ID |
| `GET` | `/analysis/contract/{contract_id}` | Get all analysis results for a contract |
| `GET` | `/analysis/` | List all analysis results |

---

## Author

 **Ayushi Singh** 
 **GitHub Profile:** https://github.com/ayus28ayushi-ai