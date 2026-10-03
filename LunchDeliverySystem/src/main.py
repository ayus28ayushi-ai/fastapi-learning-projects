from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database import create_table
from src.routes.orders import router as orders_router
from src.routes.stats import router as stats_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield

app = FastAPI(
    title = "Lunch Delivery System API",
    description = "API for managing the delivering and tracking order statuses",
    version="1.0.0",
    lifespan = lifespan
)

app.include_router(orders_router)
app.include_router(stats_router)

app.get("/health", tags=["health"])
def health_check():
    return {
        "status": "ok"
    }