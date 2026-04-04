from fastapi import APIRouter, HTTPException, Depends
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session
from database import get_db
from schemas.book import BookCreate, BookResponse
from services import book_service
from fastapi import Response

from fastapi.responses import HTMLResponse
import math

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=list[BookResponse])
def get_books(
    author: str = None,
    status: str = None,
    sort: str = None,
    offset = 0,
    limit=10,
    db: Session = Depends(get_db)
):
    return book_service.list_books(db, author, status, sort, offset, limit)

@router.get("/pretty", response_class=HTMLResponse)
def get_books_pretty(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    page = max(1, page)
    limit = min(50, limit)

    total = book_service.get_total_books(db)

    total_pages = math.ceil(total / limit)

    if page > total_pages:
        page = total_pages if total_pages > 0 else 1

    offset = (page - 1) * limit

    books = book_service.list_books(db, offset=offset, limit=limit)

    html = f"<h1>Page {page} / {total_pages}</h1><ul>"

    for b in books:
        html += f"<li>{b.id} — {b.title} ({b.author})</li>"

    html += "</ul>"

    html += "<br><br>"

    if page > 1:
        html += f'<a href="/books/pretty?page={page - 1}&limit={limit}">⬅ Prev</a> '

    if page < total_pages:
        html += f'<a href="/books/pretty?page={page + 1}&limit={limit}">Next ➡</a>'

    return html

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = book_service.get_book(book_id, db)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=BookResponse, status_code=201)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    return book_service.create_book(book, db)





@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_service.remove_book(book_id, db)
    return Response(status_code=204)