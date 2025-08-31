from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_note():
    response = client.post("/notes/", json={"title": "Test Note", "content": "This is a test"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Note"
    assert "id" in data

def test_get_notes():
    response = client.get("/notes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
