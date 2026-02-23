from fastapi import APIRouter, HTTPException
from uuid import UUID
from schemas.book import BookCreate, BookResponse
from services import book_service

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=list[BookResponse])
async def get_books(author: str = None, status: str = None, sort: str = None):
    return await book_service.list_books(author, status, sort)


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: UUID):
    book = await book_service.get_book(book_id)
    if not book:
        raise HTTPException(404, "Book not found")
    return book


@router.post("/", response_model=BookResponse, status_code=201)
async def add_book(book: BookCreate):
    return await book_service.create_book(book)


@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: UUID):
    await book_service.remove_book(book_id)