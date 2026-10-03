from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

# a table
class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    reviewer_name: str
    movie_name:str = Field(index=True)  #so we can easily search based on the movie name
    rating:int = Field(le=5, ge=1)
    comment: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# just a validator
class ReviewCreate(SQLModel):
    reviewer_name: str
    movie_name:  str
    rating: int = Field(ge=1, le=5)
    comment: str

class ReviewRead(SQLModel):
    id:int
    reviewer_name: str
    movie_name: str
    rating: int
    comment:str
    created_at: datetime

class ReviewUpdate(SQLModel):
    rating: Optional[int] = Field(default=None, le=5, ge=1)
    comment: Optional[str]

class  ReviewAverageRead(SQLModel):
    movie_name: str
    average_rating: float | None
    total_reviews: int

class ReviewListRead(SQLModel):
    skip: int
    limit: int
    reviews: list[ReviewRead]
     