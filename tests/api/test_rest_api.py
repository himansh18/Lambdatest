
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def test_get_posts_returns_list():
    response = requests.get(f"{BASE_URL}/posts", timeout=15)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_get_single_post_matches_schema():
    response = requests.get(f"{BASE_URL}/posts/1", timeout=15)

    assert response.status_code == 200
    post = response.json()

    assert isinstance(post["id"], int)
    assert isinstance(post["userId"], int)
    assert isinstance(post["title"], str)
    assert isinstance(post["body"], str)


def test_create_post():
    payload = {
        "title": "TestMu API test",
        "body": "Created by pytest",
        "userId": 1,
    }

    response = requests.post(
        f"{BASE_URL}/posts",
        json=payload,
        timeout=15,
    )

    assert response.status_code == 201
    created_post = response.json()
    assert created_post["title"] == payload["title"]
    assert created_post["body"] == payload["body"]
    assert created_post["userId"] == payload["userId"]
    assert "id" in created_post


def test_update_post():
    payload = {
        "id": 1,
        "title": "Updated by pytest",
        "body": "Updated test content",
        "userId": 1,
    }

    response = requests.put(
        f"{BASE_URL}/posts/1",
        json=payload,
        timeout=15,
    )

    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]


def test_partially_update_post():
    payload = {"title": "Patched by pytest"}

    response = requests.patch(
        f"{BASE_URL}/posts/1",
        json=payload,
        timeout=15,
    )

    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]


def test_delete_post():
    response = requests.delete(f"{BASE_URL}/posts/1", timeout=15)

    assert response.status_code in (200, 204)



def test_get_nonexistent_post():
    response = requests.get(f"{BASE_URL}/posts/999999", timeout=15)

    # The actual public API response for this nonexistent ID was HTTP 404.
    assert response.status_code == 404

