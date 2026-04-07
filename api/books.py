from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from database import get_db
from schemas.book import BookCreate, BookResponse
from services import book_service
from fastapi.responses import HTMLResponse
from urllib.parse import urlencode
import math

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=list[BookResponse])
def get_books(
    author: str = None,
    status: str = None,
    sort: str = None,
    offset: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    offset = max(0, offset)
    limit = min(50, max(1, limit))
    return book_service.list_books(db, author, status, sort, offset, limit)


@router.get("/pretty", response_class=HTMLResponse)
def get_books_pretty(
    page: int = 1,
    limit: int = 10,
    author: str = None,
    status: str = None,
    sort: str = None,
    db: Session = Depends(get_db)
):
    page = max(1, page)
    limit = min(50, max(1, limit))

    total = book_service.get_total_books(db)
    total_pages = math.ceil(total / limit) if total > 0 else 1

    if page > total_pages:
        page = total_pages if total_pages > 0 else 1

    offset = (page - 1) * limit

    books = book_service.list_books(
        db, author=author, status=status, sort=sort, offset=offset, limit=limit
    )

    html = "<h1>Бібліотека (Offset Pagination)</h1>"

    html += f"""
    <form method="get" action="/books/pretty">
        <label>Автор:</label>
        <input type="text" name="author" value="{author or ''}"><br><br>

        <label>Статус:</label>
        <input type="text" name="status" value="{status or ''}"><br><br>

        <label>Сортування:</label>
        <select name="sort">
            <option value="" {"selected" if not sort else ""}>За замовчуванням (id)</option>
            <option value="title" {"selected" if sort == "title" else ""}>За назвою</option>
            <option value="year" {"selected" if sort == "year" else ""}>За роком</option>
        </select><br><br>

        <label>Ліміт:</label>
        <input type="number" name="limit" value="{limit}" min="1" max="50"><br><br>

        <button type="submit">Застосувати</button>
    </form>
    <hr>
    """

    html += f"<h3>Page {page} / {total_pages}</h3><ul>"

    if not books:
        html += "<li>Книг не знайдено.</li>"
    else:
        for b in books:
            html += f"<li><b>ID: {b.id}</b> — {b.title} ({b.author}) - {b.year} - {b.status}</li>"

    html += "</ul><br>"

    def build_url(p):
        params = {"page": p, "limit": limit}
        if author: params["author"] = author
        if status: params["status"] = status
        if sort: params["sort"] = sort
        return f"/books/pretty?{urlencode(params)}"

    html += '<a href="/books/pretty">🏠 На початок</a><br><br>'

    if page > 1:
        html += f'<a href="{build_url(page - 1)}">⬅ Prev</a> '

    if page < total_pages:
        html += f'<a href="{build_url(page + 1)}">Next ➡</a>'
    else:
        html += "<span>Це остання сторінка</span>"

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