from sqlalchemy.orm import Session
from models.book_model import Book
from schemas.book import BookCreate

def count_books(db):
    return db.query(Book).count()

def get_all_books(db: Session, author=None, status=None, sort=None, offset=0, limit=10):
    query = db.query(Book)

    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))

    if status:
        query = query.filter(Book.status == status)

    if sort == "title":
        query = query.order_by(Book.title)
    elif sort == "year":
        query = query.order_by(Book.year)

    return query.offset(offset).limit(limit).all()

def get_book_by_id(book_id: int, db: Session):
    return db.query(Book).filter(Book.id == book_id).first()

def add_book(book_data: BookCreate, db: Session):
    new_book = Book(
        title=book_data.title,
        author=book_data.author,
        description=book_data.description,
        year=book_data.year,
        status=book_data.status
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def delete_book(book_id: int, db: Session):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return None
    db.delete(book)
    db.commit()
    return book