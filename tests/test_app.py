import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    # Test successful signup
    response = client.post("/activities/Chess Club/signup", params={"email": "test@example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "Signed up test@example.com for Chess Club"}

    # Test duplicate signup
    response = client.post("/activities/Chess Club/signup", params={"email": "test@example.com"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}

    # Test non-existent activity
    response = client.post("/activities/NonExistent/signup", params={"email": "test@example.com"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_from_activity():
    # First signup
    client.post("/activities/Programming Class/signup", params={"email": "unregister@example.com"})

    # Test successful unregister
    response = client.delete("/activities/Programming Class/unregister", params={"email": "unregister@example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "Unregistered unregister@example.com from Programming Class"}

    # Test unregister not signed up
    response = client.delete("/activities/Programming Class/unregister", params={"email": "notsigned@example.com"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is not signed up for this activity"}

    # Test non-existent activity
    response = client.delete("/activities/NonExistent/unregister", params={"email": "test@example.com"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200  # Serves the static index.html
    assert "Mergington High School" in response.text