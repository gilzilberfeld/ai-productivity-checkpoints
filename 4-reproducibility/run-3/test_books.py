import requests

BASE_URL = "http://127.0.0.1:5000"


class TestBookCreation:
    def test_create_valid_book(self):
        response = requests.post(
            f"{BASE_URL}/books", json={"title": "Clean Code", "author": "Robert Martin"}
        )
        assert response.status_code == 201
        assert response.json()["title"] == "Clean Code"

    def test_create_book_with_unicode(self):
        title = "Ótimo livro 书很好 🌟"
        response = requests.post(f"{BASE_URL}/books", json={"title": title, "author": "Автор"})
        assert response.status_code == 201
        assert response.json()["title"] == title
        assert response.json()["author"] == "Автор"

    def test_create_book_with_very_long_title(self):
        response = requests.post(
            f"{BASE_URL}/books", json={"title": "A" * 10000, "author": "Someone"}
        )
        assert response.status_code != 500

    def test_create_book_without_required_fields(self):
        assert requests.post(f"{BASE_URL}/books", json={}).status_code == 400


class TestBookRetrieval:
    def test_get_existing_book(self):
        book = requests.post(
            f"{BASE_URL}/books", json={"title": "Refactoring", "author": "Martin Fowler"}
        ).json()
        response = requests.get(f"{BASE_URL}/books/{book['id']}")
        assert response.status_code == 200
        assert response.json()["title"] == "Refactoring"

    def test_get_nonexistent_book(self):
        response = requests.get(f"{BASE_URL}/books/999999")
        assert response.status_code == 404
        assert "error" in response.json()


class TestBookDeletion:
    def test_delete_existing_book(self):
        book = requests.post(
            f"{BASE_URL}/books", json={"title": "TDD", "author": "Kent Beck"}
        ).json()
        response = requests.delete(f"{BASE_URL}/books/{book['id']}")
        assert response.status_code in (200, 204)

    def test_delete_nonexistent_book(self):
        assert requests.delete(f"{BASE_URL}/books/999999").status_code == 404


class TestBookWorkflow:
    def test_create_get_delete_get(self):
        book = requests.post(
            f"{BASE_URL}/books", json={"title": "Working Effectively", "author": "Feathers"}
        ).json()

        assert requests.get(f"{BASE_URL}/books/{book['id']}").status_code == 200

        requests.delete(f"{BASE_URL}/books/{book['id']}")

        assert requests.get(f"{BASE_URL}/books/{book['id']}").status_code == 404
