from fastapi import FastAPI
from database import create_tables
from routes.user import router as user_router
from routes.books import  router as book_router
from contextlib import asynccontextmanager
import models

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    yield

app = FastAPI(
    title="Book Reselling Platform",
    description="A platform to resell and buy used books",
    lifespan=lifespan
)

app.include_router(user_router)
app.include_router(book_router)

@app.get("/")
def root():
    return {"message": "Welcome to book reselling API"}