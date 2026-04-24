from app.schemas.review import Review
from fastapi import APIRouter, Path, HTTPException
    from schemas.book import Book, books
    from typing import Annotated
    from schemas.review import Review

    books_router = APIRouter(prefix="/books", tags=["books"])

    @books_router.get("/")
    def get_all_books() -> list[Book]:
        """Returns the list ok avaible books."""
        return list(books.values())

    @books_router.get("/{id}")
    def get_book_by_id(id: Annotated[id, Path(description="The id of the book to retrieve")]
                       )-> Book:
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
            books[id].review=review.review
            return "Review added successfully"
        except KeyError:
            raise HTTPException(status_code=404, detail="Book not found")


