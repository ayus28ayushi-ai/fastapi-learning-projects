from fastapi import FastAPI
from app.routes import router as router

app = FastAPI(
    title="Netra Vision API",
    description="AI-powered crop detection using Gemini Vision",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
async def root():
    return {
        "app": "netra-vision",
        "version": "1.0.0",
        "endpoints":{
            "POST /upload": "Upload an image for disease detection",
            "POST /uploads": "Upload multiple images for disease detection",
            "GET /analysis": "Retrieve the list of all the analyses performed",
            "GET /analysis/{analysis_id}": "Retrieve details of a specific analysis"
        }
    }