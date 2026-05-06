from fastapi import APIRouter, Path, HTTPException, Query
from typing import Annotated
from sqlmodel import select, delete

# Importazioni pulite e corrette
from app.schemas.book import BookDB, BookPublic, BookCreate
from app.schemas.review import Review
from app.data.db import SessionDep

books_router = APIRouter(prefix="/books", tags=["books"])


@books_router.get("/", response_model=list[BookPublic])
def get_all_books(
        session: SessionDep,
        sort: Annotated[bool, Query(description="Sort books by their reviews")] = False
):
    """Returns the list of available books."""
    books = session.exec(select(BookDB)).all()
    if books:
        return books
    raise HTTPException(status_code=404, detail="Books not found")


@books_router.get("/{id}", response_model=BookPublic)
def get_book_by_id(
        session: SessionDep,
        id: Annotated[int, Path(description="The id of the book to retrieve")]
):
    """Returns the book with the given id"""
    book = session.get(BookDB, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@books_router.post("/{id}/review")
def add_review(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the book to add")],
        review: Review
):
    """Adds a review to the book with the given ID"""
    book = session.get(BookDB, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.review = review.review
    session.add(book)
    session.commit()
    return {"message": "Review added successfully"}


@books_router.post("/")
def add_book(session: SessionDep, book: BookCreate):
    """Adds a book to the database"""
    book_entry = BookDB.model_validate(book)
    session.add(book_entry)
    session.commit()
    return {"message": "Book added successfully"}


@books_router.put("/{id}")
def replace_book(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the book to update")],
        book_update: BookCreate
):
    """Replace the book with the given ID"""
    book = session.get(BookDB, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.title = book_update.title
    book.author = book_update.author
    book.review = book_update.review

    session.add(book)
    session.commit()
    return {"message": "Book replaced successfully"}


@books_router.delete("/")
def delete_all_books(session: SessionDep):
    """Deletes all the stored books"""
    session.exec(delete(BookDB))
    session.commit()
    return {"message": "All books deleted successfully"}


@books_router.delete("/{id}")
def delete_book(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the book to delete")]
):
    """Deletes the book with the given ID"""
    book = session.get(BookDB, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    session.delete(book)
    session.commit()
    return {"message": "Book deleted successfully"}