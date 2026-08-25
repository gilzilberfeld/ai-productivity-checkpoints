import requests

BASE_URL = "http://127.0.0.1:5000"


def create_book(title="Clean Code", author="Robert Martin"):
    return requests.post(f"{BASE_URL}/books", json={"title": title, "author": author})


def test_create_book_returns_201():
    response = create_book()
    assert response.status_code == 201


def test_create_book_returns_all_fields():
    body = create_book().json()
    assert "id" in body
    assert "title" in body
    assert "author" in body


def test_create_book_echoes_input():
    body = create_book("Refactoring", "Martin Fowler").json()
    assert body["title"] == "Refactoring"
    assert body["author"] == "Martin Fowler"


def test_create_book_missing_title_returns_400():
    response = requests.post(f"{BASE_URL}/books", json={"author": "Robert Martin"})
    assert response.status_code == 400


def test_create_book_missing_author_returns_400():
    response = requests.post(f"{BASE_URL}/books", json={"title": "Clean Code"})
    assert response.status_code == 400


def test_create_book_empty_body_returns_400():
    response = requests.post(f"{BASE_URL}/books", json={})
    assert response.status_code == 400


def test_get_book_returns_created_book():
    book = create_book().json()
    response = requests.get(f"{BASE_URL}/books/{book['id']}")
    assert response.status_code == 200
    assert response.json() == book


def test_get_unknown_book_returns_404():
    response = requests.get(f"{BASE_URL}/books/999999")
    assert response.status_code == 404


def test_delete_book_returns_204():
    book = create_book().json()
    response = requests.delete(f"{BASE_URL}/books/{book['id']}")
    assert response.status_code == 204


def test_deleted_book_is_gone():
    book = create_book().json()
    requests.delete(f"{BASE_URL}/books/{book['id']}")
    assert requests.get(f"{BASE_URL}/books/{book['id']}").status_code == 404


def test_delete_unknown_book_returns_404():
    response = requests.delete(f"{BASE_URL}/books/999999")
    assert response.status_code == 404
