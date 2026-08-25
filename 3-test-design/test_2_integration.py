import pytest
import requests

# Assumes both services are already running:
BASE_URL = "http://127.0.0.1:5000"
MODERATION_URL = "http://127.0.0.1:5001"
AUTH_HEADER = {"Authorization": "Bearer token-user-1"}


@pytest.fixture(autouse=True)
def reset_moderation():
    yield
    requests.post(f"{MODERATION_URL}/admin/reset")


def moderation_mode(config):
    requests.post(f"{MODERATION_URL}/admin/configure", json=config)


def new_book():
    return requests.post(
        f"{BASE_URL}/books", json={"title": "Clean Code", "author": "Robert Martin"}
    ).json()


def post_review(book_id, rating=5, comment="Excellent"):
    return requests.post(
        f"{BASE_URL}/books/{book_id}/reviews",
        json={"rating": rating, "comment": comment},
        headers=AUTH_HEADER,
    )


def test_approved_review_is_saved():
    book = new_book()

    # The real moderation service, in its default approving mode
    response = post_review(book["id"])
    assert response.status_code == 201

    # It went out to moderation, came back, and got written down
    reviews = requests.get(f"{BASE_URL}/books/{book['id']}/reviews").json()
    assert len(reviews) == 1
    assert reviews[0] == response.json()


def test_rejected_review_is_refused_and_not_saved():
    book = new_book()

    # Tell the real service to reject
    moderation_mode({"mode": "reject", "reject_reason": "Offensive language"})

    response = post_review(book["id"], rating=1, comment="terrible")

    # The server refuses the review and passes the reason through
    assert response.status_code == 422
    assert response.json()["reason"] == "Offensive language"

    # And nothing was saved
    assert requests.get(f"{BASE_URL}/books/{book['id']}/reviews").json() == []


def test_moderation_timeout_returns_504_and_saves_nothing():
    book = new_book()

    # The real service sleeps past the server's 3-second timeout. We wait for it.
    moderation_mode({"mode": "delay", "delay_seconds": 5})

    response = post_review(book["id"])

    assert response.status_code == 504
    assert requests.get(f"{BASE_URL}/books/{book['id']}/reviews").json() == []
