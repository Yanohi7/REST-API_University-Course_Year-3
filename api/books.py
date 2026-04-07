from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse

from database import get_db
from schemas.book import BookCreate, BookResponse, PaginatedBookResponse
from services import book_service

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=PaginatedBookResponse)
def get_books(
    author: str = None,
    status: str = None,
    sort: str = None,
    cursor: str = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    limit = min(50, limit)
    return book_service.list_books(db, author, status, sort, cursor, limit)


@router.get("/pretty", response_class=HTMLResponse)
def get_books_pretty(
    author: str = None,
    status: str = None,
    sort: str = None,
    cursor: str = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    limit = min(50, limit)

    data = book_service.list_books(
        db,
        author=author,
        status=status,
        sort=sort,
        cursor=cursor,
        limit=limit
    )

    books = data["items"]
    next_cursor = data["next_cursor"]
    has_more = data["has_more"]

    html = "<h1>Бібліотека (Cursor Pagination)</h1>"

    html += """
    <form method="get" action="/books/pretty">
        <label>Автор:</label>
        <input type="text" name="author" value="{author}"><br><br>

        <label>Статус:</label>
        <input type="text" name="status" value="{status}"><br><br>

        <label>Сортування:</label>
        <select name="sort">
            <option value="" {sort_default}>За замовчуванням (id)</option>
            <option value="title" {sort_title}>За назвою</option>
            <option value="year" {sort_year}>За роком</option>
        </select><br><br>

        <label>Ліміт:</label>
        <input type="number" name="limit" value="{limit}" min="1" max="50"><br><br>

        <button type="submit">Застосувати</button>
    </form>
    <hr>
    """.format(
        author=author or "",
        status=status or "",
        limit=limit,
        sort_default="selected" if not sort else "",
        sort_title="selected" if sort == "title" else "",
        sort_year="selected" if sort == "year" else ""
    )

    html += "<ul>"

    if not books:
        html += "<li>Книг немає або ви дійшли до кінця.</li>"
    else:
        for b in books:
            html += f"<li><b>ID: {b.id}</b> — {b.title} ({b.author}) - {b.year} - {b.status}</li>"

    html += "</ul><br>"

    base_params = []
    if author:
        base_params.append(f"author={author}")
    if status:
        base_params.append(f"status={status}")
    if sort:
        base_params.append(f"sort={sort}")
    base_params.append(f"limit={limit}")

    base_query = "&".join(base_params)

    html += '<a href="/books/pretty">🏠 На початок</a><br><br>'

    if has_more and next_cursor:
        next_url = f"/books/pretty?{base_query}&cursor={next_cursor}"
        html += f'<a href="{next_url}">Далі ➡</a>'
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
    book = book_service.remove_book(book_id, db)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return Response(status_code=204)