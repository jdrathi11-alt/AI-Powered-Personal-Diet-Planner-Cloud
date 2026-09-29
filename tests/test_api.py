import os
import tempfile
import pytest

os.environ["DATABASE_MODE"] = "sqlite"

from backend.app import app
from backend import db

@pytest.fixture()
def client(tmp_path, monkeypatch):
    dbfile = tmp_path / "test.db"
    monkeypatch.setattr(db, "db_path", lambda: dbfile)
    db.init_db()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def register(client, email="a@example.com"):
    return client.post("/api/register", json={
        "name": "Demo User", "email": email, "password": "password123"
    })

def login(client, email="a@example.com"):
    return client.post("/api/login", json={
        "email": email, "password": "password123"
    })

def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}

def test_health(client):
    assert client.get("/api/health").status_code == 200

def test_register_and_duplicate(client):
    assert register(client).status_code == 201
    assert register(client).status_code == 409

def test_login(client):
    register(client)
    response = login(client)
    assert response.status_code == 200
    assert response.json["token"]

def test_invalid_login(client):
    register(client)
    response = client.post("/api/login", json={
        "email": "a@example.com", "password": "wrongpass"
    })
    assert response.status_code == 401

def test_protected_profile(client):
    register(client)
    token = login(client).json["token"]
    assert client.get("/api/profile", headers=auth_headers(token)).status_code == 200

def test_profile_and_plan(client):
    register(client)
    token = login(client).json["token"]
    headers = auth_headers(token)
    response = client.put("/api/profile", headers=headers, json={
        "age": 20, "height_cm": 170, "weight_kg": 65,
        "activity_level": "moderate",
        "dietary_preference": "vegetarian",
        "goal": "General balanced eating",
        "allergies": ""
    })
    assert response.status_code == 200
    plan = client.post("/api/generate-plan", headers=headers)
    assert plan.status_code == 200
    assert "breakfast" in plan.json["plan"]

def test_user_isolation(client):
    register(client, "a@example.com")
    token_a = login(client, "a@example.com").json["token"]
    register(client, "b@example.com")
    token_b = login(client, "b@example.com").json["token"]

    headers_a = auth_headers(token_a)
    headers_b = auth_headers(token_b)
    client.put("/api/profile", headers=headers_a, json={"goal": "A goal"})
    client.put("/api/profile", headers=headers_b, json={"goal": "B goal"})

    a = client.get("/api/profile", headers=headers_a).json["profile"]
    b = client.get("/api/profile", headers=headers_b).json["profile"]
    assert a["goal"] == "A goal"
    assert b["goal"] == "B goal"
