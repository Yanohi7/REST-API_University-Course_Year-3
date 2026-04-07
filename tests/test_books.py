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

    data = res.json()
    assert isinstance(data, dict)
    assert "items" in data
    assert "next_cursor" in data
    assert "has_more" in data
    assert isinstance(data["items"], list)


def test_delete_book_idempotent():
    res = client.delete("/books/999999")
    assert res.status_code in [204, 404]


def test_get_books_with_limit_cursor():
    for i in range(5):
        client.post("/books/", json={
            "title": f"Book {i}",
            "author": "Test",
            "year": 2000 + i,
            "status": "available"
        })

    first_res = client.get("/books/?limit=2")
    assert first_res.status_code == 200

    first_data = first_res.json()
    assert isinstance(first_data, dict)
    assert "items" in first_data
    assert len(first_data["items"]) == 2

    next_cursor = first_data["next_cursor"]

    if next_cursor:
        second_res = client.get(f"/books/?limit=2&cursor={next_cursor}")
        assert second_res.status_code == 200

        second_data = second_res.json()
        assert isinstance(second_data, dict)
        assert "items" in second_data
        assert len(second_data["items"]) <= 2