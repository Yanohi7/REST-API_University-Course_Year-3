from uuid import uuid4
from models.book_model import BOOKS_DB
from schemas.book import BookCreate


async def get_all_books():
    return BOOKS_DB

async def get_book_by_id(book_id: int):
    return next((b for b in BOOKS_DB if b["id"] == book_id), None)

async def add_book(book_data: dict):
    book_data["id"] = uuid4()
    BOOKS_DB.append(book_data)
    return book_data

async def delete_book(book_id):
    global BOOKS_DB
    before = len(BOOKS_DB)
    BOOKS_DB[:] = [b for b in BOOKS_DB if b["id"] != book_id]
    return len(BOOKS_DB)



