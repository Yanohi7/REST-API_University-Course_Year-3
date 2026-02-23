from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_add_book():
    res = client.post("/books/", json={
        "title": "1984",
        "author": "Orwell",
        "year": 1949,
        "status": "available"
    })
    assert res.status_code == 201
    assert "id" in res.json()


def test_get_books():
    res = client.get("/books/")
    assert res.status_code == 200


def test_delete_book_idempotent():
    res = client.delete("/books/00000000-0000-0000-0000-000000000000")
    assert res.status_code == 204