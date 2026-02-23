from repository import book_repo

async def list_books(author=None, status=None, sort=None):
    books = await book_repo.get_all_books()

    if author:
        books = [b for b in books if author.lower() in b["author"].lower()]

    if status:
        books = [b for b in books if b["status"] == status]

    if sort == "title":
        books.sort(key=lambda x: x["title"])
    elif sort == "year":
        books.sort(key=lambda x: x["year"])

    return books

async def get_book(book_id):
    return await book_repo.get_book_by_id(book_id)

async def create_book(book):
    return await book_repo.add_book(book.model_dump())

async def remove_book(book_id):
    return await book_repo.delete_book(book_id)
