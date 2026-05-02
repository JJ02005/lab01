from fastapi import APIRouter, Path, HTTPException, Query
from typing import Annotated
from app.schemas.book import Book, books # Assicurati che il path sia corretto
from app.schemas.review import Review

# 1. Il router deve stare a inizio riga
books_router = APIRouter(prefix="/books", tags=["books"])

@books_router.get("/")
def get_all_books(
        sort: Annotated[bool, Query(description="Sort books by their reviews")] = False
)->list[Book]:
    """Returns the list of available books."""
    if sort:
       return  sorted(books.values(), key=lambda book: book.review)
    else:
        return list(books.values())

@books_router.get("/{id}")
# 2. Corretto 'id' in 'int' dentro Annotated
def get_book_by_id(id: Annotated[int, Path(description="The id of the book to retrieve")]) -> Book:
    """Returns the book with the given id"""
    try:
        return books[id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found")

@books_router.post("/{id}/review")
def add_review(
    id: Annotated[int, Path(description="The ID of the book to add")],
    review: Review
):
    """Adds a review to the book with the given ID"""
    try:
        # 3. Assicurati che l'oggetto Book abbia il campo .review
        books[id].review = review.review
        return {"message": "Review added successfully"} # Meglio restituire un dizionario (JSON)
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found")

@books_router.post("/")
def add_book(book: Book):
    """Adds a book to the database"""
    if book.id  in books:
        raise HTTPException(status_code=403, detail="Book already exists")
    books[book.id] = book
    return {"message": "Book added successfully"}

@books_router.put("/{id}")
def replace_book(
        id: Annotated[int, Path(description="The ID of the book to update")],
        book: Book
        ):
    """Replace the book with the given ID"""
    if not id in books:
        raise HTTPException(status_code=404, detail="Book not found")
    books[id] = book
    return "Book replaced successfully"

@books_router.delete("/")
def delete_all_books():
    "Deletes all the stored books"
    books.clear()
    return "All books deleted successfully"

@books_router.delete("/{id}")
def delete_book(
    id: Annotated[int, Path(description="The ID of the book to delete")]
):
    """Deletes the book with the given ID"""
    if not id in books:
        raise HTTPException(status_code=404, detail="Book not found")
    del books[id]
    return "Book deleted successfully"
