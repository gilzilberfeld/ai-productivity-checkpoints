from unittest.mock import Mock, patch

import pytest
import requests as http

from server.app import create_app

AUTH_HEADER = {"Authorization": "Bearer token-user-1"}


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def moderation_says(payload, status=200):
    fake = Mock()
    fake.status_code = status
    fake.json.return_value = payload
    return fake


def test_rejected_review_is_refused_and_not_saved(client):
    # A book to hang the review on
    book = client.post("/books", json={"title": "Clean Code", "author": "Robert Martin"}).get_json()

    # The moderation service never runs. This stands in for it.
    stub = moderation_says({"approved": False, "reason": "Offensive language"})
    with patch("routes_reviews.http.post", return_value=stub):
        response = client.post(
            f"/books/{book['id']}/reviews",
            json={"rating": 1, "comment": "terrible"},
            headers=AUTH_HEADER,
        )

    # The server refuses the review and says why
    assert response.status_code == 422
    assert response.get_json()["reason"] == "Offensive language"

    # And nothing was saved
    assert client.get(f"/books/{book['id']}/reviews").get_json() == []


def test_moderation_timeout_returns_504_and_saves_nothing(client):
    book = client.post("/books", json={"title": "Refactoring", "author": "Martin Fowler"}).get_json()

    # No 3-second wait. The timeout is raised on the spot.
    with patch("routes_reviews.http.post", side_effect=http.exceptions.Timeout):
        response = client.post(
            f"/books/{book['id']}/reviews",
            json={"rating": 5, "comment": "Great"},
            headers=AUTH_HEADER,
        )

    assert response.status_code == 504
    assert client.get(f"/books/{book['id']}/reviews").get_json() == []
