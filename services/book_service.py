from sqlalchemy.orm import Session
from repository import book_repo
from schemas.book import BookCreate


def get_total_books(db: Session):
    return book_repo.count_books(db)


def list_books(db: Session, author=None, status=None, sort=None, cursor=None, limit=10):
    books = book_repo.get_all_books(
        db=db,
        author=author,
        status=status,
        sort=sort,
        cursor=cursor,
        limit=limit
    )

    has_more = len(books) > limit

    if has_more:
        visible_books = books[:limit]
        last_book = visible_books[-1]

        if sort == "title":
            next_cursor = f"{last_book.title},{last_book.id}"
        elif sort == "year":
            next_cursor = f"{last_book.year},{last_book.id}"
        else:
            next_cursor = str(last_book.id)
    else:
        visible_books = books
        next_cursor = None

    return {
        "items": visible_books,
        "next_cursor": next_cursor,
        "has_more": has_more
    }


def get_book(book_id: int, db: Session):
    return book_repo.get_book_by_id(book_id, db)


def create_book(book: BookCreate, db: Session):
    return book_repo.add_book(book, db)


def remove_book(book_id: int, db: Session):
    return book_repo.delete_book(book_id, db)