from fastapi import FastAPI
from app.routes.planner import router as planner_router
from app.routes.stream import router as stream_router

app = FastAPI(
    title="Travel Planner API",
    description="Aggregate travel data from multiple sources to provide single plan with SSE support",
    version="1.0.0"
)

app.include_router(planner_router)
app.include_router(stream_router)

@app.get("/", summary="API Root", description="Get API information and available endpoints")
async def root():
    return {
        "app": "Travel Planner API",
        "version": "1.0.0",
        "endpoints":{
            "POST /plan": "Create a travel plan (Aggregated)",
            "POST /plan/stream": "Stream the travel plan (SSE)",
            "GET /plan/cache-stats": "Get cache statistics",
            "DELETE /plan/cache": "Clear the cache"
        }
    }