from fastapi import Depends, HTTPException, APIRouter, Query
from typing import Optional
from database import get_session
from sqlmodel import Session, select

from models.books import BodyRead, BookCreate, Books, BookUpdate

from auth import verify_api_key

router = APIRouter(prefix="/books", tags=["books"])
@ router.get("/", response_model=list[BodyRead])
def list_book(
    title: Optional[str] = Query(default=None, description="Query using book title"),
    author: Optional[str] = Query(default= None, description="Query using author name"),
    session: Session = Depends(get_session)
):
    query = select(Books).where(
        Books.is_sold == False
    )

    if title:
        query = query.where(Books.title.contains(title))
    if author:
        query = query.where(Books.author.contains(author))
    books = session.exec(query).all()
    return books


@router.post("/", response_model=BodyRead)
def create_book(
    book_data: BookCreate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)
):
    book = Books.model_validate(book_data)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.patch("/{book_id}", response_model=BodyRead)
def update_book(
    book_id: int,
    updates: BookUpdate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)
):
    book = session.get(Books, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book_data = updates.model_dump(exclude_unset=True)
    for key, val in book_data.items():
        setattr(book, key, val)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@router.patch("/{book_id}/sold", response_model=BodyRead)
def book_sold(
    book_id: int,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)
):
    book = session.get(Books, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book with this id doesnt exist")

    book.is_sold = True
    session.add(book)
    session.commit()
    session.refresh(book)
    return book
 