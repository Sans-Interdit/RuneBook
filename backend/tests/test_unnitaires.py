from flask import Flask
from backend.api import bp

app = Flask(__name__)
app.register_blueprint(bp)  # ← indispensable pour que /login existe

def test_login():
    try:
        with app.test_client() as client:
            response = client.post("/api/login", json={
                "email": "test@exemple.com",
                "password": "strongPWD123"
            })
            assert response.status_code == 200
            print("✅ Login réussi")

    except AssertionError:
        print("❌ test_login a échoué")

def test_getGuides():
    try:
        with app.test_client() as client:
            response = client.get("/api/get-guides")
            assert response.status_code == 200
            print("✅ Guides obtenus")

    except AssertionError:
        print("❌ test_getGuides a échoué")

if __name__ == "__main__":
    test_login()
    test_getGuides()

