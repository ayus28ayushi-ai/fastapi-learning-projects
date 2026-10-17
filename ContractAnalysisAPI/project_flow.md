graph TD
    Client([Client / Postman]) -->|HTTP POST Request| FastAPI[FastAPI Route Handler]
    FastAPI -->|Fetch contract by ObjectId| MongoDB[(MongoDB Database)]
    MongoDB -->|Returns raw contract text| FastAPI
    FastAPI -->|Passes text and prompt template| Service[Analysis Service]
    Service -->|Async API Call via google-genai SDK| Gemini[Google Gemini AI]
    Gemini -->|Returns strict JSON string response| Service
    Service -->|json.loads & Pydantic Validation| Models[Pydantic Models: ClauseAnalysis, RiskFlag, AnalysisResult]
    Models -->|Structured Python Object| FastAPI
    FastAPI -->|Validated JSON Response| Client