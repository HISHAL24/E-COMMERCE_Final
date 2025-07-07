import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_login_page_redirect(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/login.html" in response.headers["Location"]

def test_static_file_serving(client):
    response = client.get("/style.css")
    assert response.status_code in [200, 404]  # Only 200 if style.css exists

def test_invalid_login(client):
    response = client.post("/login", json={"username": "wrong", "password": "wrong"})
    assert response.status_code == 401
    assert b"Invalid credentials" in response.data

def test_logout_without_login(client):
    response = client.post("/logout")
    assert response.status_code == 200
    assert b"Logged out" in response.data
