from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.routes.contracts import router as contract_router
from app.routes.analysis import router as analysis_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Advocate Contract API",
    description="AI-powered contract Analysis API",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return{
        "app": "Contract Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "POST /contracts/upload" : "Upload a PDF or TXT contract for analysis",
            "GET /contracts/": "Rectrieve a list of all the uploaded contracts",
            "GET /contracts/{id}": "Retrieve details of a specific contract by ID",
            "POST /analysis/analyse/{contract_id}": "Analyze a contract using AI and return insights",
            "GET /analysis/{analysis_id}": "Retrieve the results of a specific anaylisis by ID",
            "GET /analysis/contract/{contract_id}": "Retrieve a list of all analysis performed for a specific contract"
        }
    }

app.include_router(contract_router)
app.include_router(analysis_router)