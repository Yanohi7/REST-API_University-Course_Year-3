from sqlalchemy.orm import Session
from repository import book_repo
from schemas.book import BookCreate

def get_total_books(db):
    return book_repo.count_books(db)

def list_books(db: Session, author=None, status=None, sort=None, offset=0, limit=10):
    return book_repo.get_all_books(
        db=db,
        author=author,
        status=status,
        sort=sort,
        offset=offset,
        limit=limit
    )

def get_book(book_id: int, db: Session):
    return book_repo.get_book_by_id(book_id, db)

def create_book(book: BookCreate, db: Session):
    return book_repo.add_book(book, db)

def remove_book(book_id: int, db: Session):
    return book_repo.delete_book(book_id, db)