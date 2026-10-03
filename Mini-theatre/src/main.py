from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database import create_tables
from src.routes.reviews import router as review_router
from src.exceptions import ReviewNotFoundException, review_not_found_handler
from src import models
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("creating table")
    yield #shutdown of the app
    print("shutting down the app")

app = FastAPI(
    title="Mini-theatre",
    description="Theatre review API",
    lifespan=lifespan
)
#anything that starts with  /review will be routed here
app.include_router(review_router)

app.exception_handler(ReviewNotFoundException)(review_not_found_handler)
@app.get("/")
def root():
    return {"message": "Welcome to Mini-theatre review API"}

