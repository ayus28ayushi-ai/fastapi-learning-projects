from fastapi.responses import JSONResponse
from fastapi import Request

class ReviewNotFoundException(Exception):
    def __init__(self, review_count, movie_name):
        self.review_count = review_count
        self.movie_name = movie_name

async def review_not_found_handler(request:Request, exc: ReviewNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "no reviews  found",
            "message": f"No reviews found for the movie {exc.movie_name}",
            "movie_name": f"{exc.movie_name}"
        }
    )

class ReviewIdNotFound(Exception):
    def __init__(self, id):
        self.id = id

async def review_id_not_found_handler(request:Request, exc: ReviewIdNotFound):
    return JSONResponse(
        status_code=404,
        content={
            "error": "no reviews  found",
            "message": f"No reviews found for the id {exc.id}",
            "id": f"{exc.id}"
        }
    )