from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, func
from src.models import ReviewCreate, Review, ReviewRead, ReviewUpdate, ReviewAverageRead, ReviewListRead
from src.database import get_session
from src.exceptions import ReviewNotFoundException, review_id_not_found_handler, ReviewIdNotFound

router=APIRouter(prefix="/review", tags=["review"])

@router.post("/", response_model=ReviewRead)
def  create_review(review: ReviewCreate, session:Session=Depends(get_session)):
    db_review = Review(**review.model_dump())
    """ 'review' is the data the user sent that has been validated by ReviewCreate class
        '.model_dump()' is a pydantic method taht converts the pydantic model into  a standard python dictionary
        ** is the unpacking operator and it takes the dictionary and unpacks the key-value pairs as keyword argument in a function/class
        'Review()' creates a new instance of the database table class """
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

@router.get("/", response_model=ReviewListRead)
def list_reviews(
    movie_name:str | None = Query(None, description="Filter by movie name"),
    skip: int = Query(0, ge=0, description="Number of reviews to skip"),
    limit: int = Query(10, ge=1, le=50, description="Max reviews to return"),
    session: Session = Depends(get_session)
):
    query = select(Review)

    if movie_name:
        query = query.where(Review.movie_name == movie_name)

    query = query.offset(skip).limit(limit)

    reviews = session.exec(query).all()
    return {
        "skip": skip,
        "limit": limit,
        "reviews": reviews
    }

@router.get("/average/{movie_name}", response_model=ReviewAverageRead)
def get_avg_rating(movie_name: str, session: Session = Depends(get_session)):
    result = session.exec(
        select(func.avg(Review.rating), func.count(Review.id)).where(
            Review.movie_name == movie_name
        )
    ).first()

    avg_rating, review_count = result

    if review_count == 0:
        raise ReviewNotFoundException(review_count, movie_name)

    return {
        "movie_name": movie_name,
        "average_rating"  : avg_rating,
        "total_reviews": review_count
    }


@router.get("/{review_id}", response_model=ReviewRead)
def get_review_by_id(review_id: int, session: Session = Depends(get_session)):
    review = session.get(Review, review_id)
    if not review:
        raise ReviewIdNotFound(review_id)
    return review

@router.patch("/{review_id}", response_model=ReviewRead)
def update_review(review_id: int,update: ReviewUpdate, session: Session = Depends(get_session)):
    review = session.get(Review, review_id)
    if not review:
        raise ReviewIdNotFound(review_id)

    update_data = update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(review, key, value)

    session.add(review)
    session.commit()
    session.refresh(review)
    return review

@router.delete("/{review_id}" )
def update_review(review_id: int,update: ReviewUpdate, session: Session = Depends(get_session)):
    review = session.get(Review, review_id)
    if not review:
        raise ReviewIdNotFound(review_id)

     

    session.delete(review)
    session.commit()
  
    return {"message": "Review deleted"}
