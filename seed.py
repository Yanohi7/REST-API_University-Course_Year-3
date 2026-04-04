from database import SessionLocal
from models.book_model import Book

def seed_books():
    db = SessionLocal()
    try:
        books = []
        for i in range(1, 151):
            book = Book(
                title=f"Book {i}",
                author=f"Author {i}",
                description=f"Description for book {i}",
                year=2000 + (i % 25),
                status="available" if i % 2 == 0 else "issued"
            )
            books.append(book)

        db.add_all(books)
        db.commit()
        print("150 книг успішно додано.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_books()