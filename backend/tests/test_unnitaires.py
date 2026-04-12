from fastapi.testclient import TestClient
from backend.app import app


client = TestClient(app)

def test_login():
    response = client.post("/api/login", json={
        "email": "test@exemple.com",
        "password": "strongPWD123"
    })
    
    assert response.status_code == 200
    
    data = response.json()
    assert "id_account" in data


def test_getGuides():
    response = client.get("/api/guides")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)