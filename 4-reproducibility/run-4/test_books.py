import requests

BASE_URL = "http://127.0.0.1:5000"
BOOK = {"title": "Clean Code", "author": "Robert Martin"}


def test_create_book():
    response = requests.post(f"{BASE_URL}/books", json=BOOK)
    assert response.status_code == 201


def test_create_book_validation():
    response = requests.post(f"{BASE_URL}/books", json={"title": "Clean Code"})
    assert response.status_code == 400


def test_get_book():
    book = requests.post(f"{BASE_URL}/books", json=BOOK).json()
    response = requests.get(f"{BASE_URL}/books/{book['id']}")
    assert response.status_code == 200
    assert "title" in response.json()


def test_get_book_not_found():
    response = requests.get(f"{BASE_URL}/books/999999")
    assert response.status_code == 404


def test_delete_book():
    book = requests.post(f"{BASE_URL}/books", json=BOOK).json()
    response = requests.delete(f"{BASE_URL}/books/{book['id']}")
    assert response.status_code == 204
