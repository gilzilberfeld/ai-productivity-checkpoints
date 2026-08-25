import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"


@pytest.fixture
def book():
    created = requests.post(
        f"{BASE_URL}/books", json={"title": "Clean Code", "author": "Robert Martin"}
    ).json()
    yield created
    requests.delete(f"{BASE_URL}/books/{created['id']}")


def test_full_lifecycle():
    created = requests.post(
        f"{BASE_URL}/books", json={"title": "Refactoring", "author": "Martin Fowler"}
    ).json()

    assert requests.get(f"{BASE_URL}/books/{created['id']}").json() == created

    requests.delete(f"{BASE_URL}/books/{created['id']}")

    assert requests.get(f"{BASE_URL}/books/{created['id']}").status_code == 404


def test_response_has_exactly_the_expected_fields(book):
    assert set(book.keys()) == {"id", "title", "author"}


def test_id_is_a_non_empty_string(book):
    assert isinstance(book["id"], str)
    assert book["id"] != ""


def test_get_returns_the_identical_object(book):
    assert requests.get(f"{BASE_URL}/books/{book['id']}").json() == book


@pytest.mark.parametrize(
    "payload",
    [
        {"title": "Clean Code"},
        {"author": "Robert Martin"},
        {},
        None,
    ],
)
def test_incomplete_body_is_rejected(payload):
    response = requests.post(f"{BASE_URL}/books", json=payload)
    assert response.status_code == 400


@pytest.mark.parametrize("method", ["get", "delete"])
def test_unknown_book_returns_404(method):
    response = getattr(requests, method)(f"{BASE_URL}/books/999999")
    assert response.status_code == 404


def test_consecutive_books_get_different_ids():
    first = requests.post(f"{BASE_URL}/books", json={"title": "A", "author": "X"}).json()
    second = requests.post(f"{BASE_URL}/books", json={"title": "B", "author": "Y"}).json()
    assert first["id"] != second["id"]


def test_deleting_one_book_leaves_the_other(book):
    other = requests.post(f"{BASE_URL}/books", json={"title": "B", "author": "Y"}).json()

    requests.delete(f"{BASE_URL}/books/{other['id']}")

    assert requests.get(f"{BASE_URL}/books/{book['id']}").status_code == 200
