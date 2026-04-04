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
    data = res.json()
    assert "id" in data
    assert data["title"] == "1984"


def test_get_books():
    res = client.get("/books/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_delete_book_idempotent():
    res = client.delete("/books/999999")
    assert res.status_code == 204


def test_get_books_with_limit_offset():
    for i in range(5):
        client.post("/books/", json={
            "title": f"Book {i}",
            "author": "Test",
            "year": 2000 + i,
            "status": "available"
        })

    res = client.get("/books/?limit=2&offset=1")
    assert res.status_code == 200

    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 2