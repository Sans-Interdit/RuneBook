from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_login():
    response = client.post("/api/login", json={
        "email": "test@exemple.com",
        "password": "strongPWD123"
    })
    assert response.status_code == 200

def test_getGuides():
    response = client.get("/api/get-guides")
    assert response.status_code == 200

