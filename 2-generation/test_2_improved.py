import requests

BASE_URL = "http://localhost:5000"
AUTH_HEADER = {"Authorization": "Bearer token-user-1"}


def test_add_review():
    book_data = {"title": "Clean Code", "author": "Robert Martin"}
    book = requests.post(f"{BASE_URL}/books", json=book_data).json()

    # Check response contains what was sent
    assert book["title"] == book_data["title"]
    assert book["author"] == book_data["author"]
    assert book["id"]

    # Get the book details
    response = requests.get(f"{BASE_URL}/books/{book['id']}")
    assert response.status_code == 200
    assert response.json() == book

    review_data = {
        "rating": 5,
        "comment": "Excellent book on software craftsmanship!",
        "user_id": "user-1",
    }

    response = requests.post(f"{BASE_URL}/books/{book['id']}/reviews", json=review_data, headers=AUTH_HEADER)
    assert response.status_code == 201

    # Check review data is correct
    created = response.json()
    assert created["rating"] == review_data["rating"]
    assert created["comment"] == review_data["comment"]
    assert created["book_id"] == book["id"]
    assert created["user_id"] == "user-1"
    assert created["id"]

    # Get review data
    response = requests.get(f"{BASE_URL}/books/{book['id']}/reviews")
    assert response.status_code == 200

    reviews = response.json()
    assert len(reviews) == 1
    assert reviews[0] == created

    requests.delete(f"{BASE_URL}/books/{book['id']}")
