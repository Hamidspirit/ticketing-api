import pytest
from app import create_app
from app.models import db

@pytest.fixture()
def client():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
    client = app.test_client()
    yield client
    with app.app_context():
        db.drop_all()

def auth_token(client):
    client.post("/auth/register", json={"username": "bob", "password": "secret123"})
    resp = client.post("/auth/login", json={"username": "bob", "password": "secret123"})
    return resp.get_json()["access_token"]

def test_create_and_list_tickets(client):
    token = auth_token(client)
    # Create
    resp = client.post("/tickets",
                       json={"title": "Bug A", "description": "Fix API bug", "priority": "high"},
                       headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201
    ticket_info = resp.get_json()
    assert "ticket_id" in ticket_info
    assert "created_at" in ticket_info

    # List
    resp = client.get("/tickets", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data["tickets"]) == 1
    assert data["tickets"][0]["priority"] == "high"

def test_filters(client):
    token = auth_token(client)
    # Create two tickets
    client.post("/tickets", json={"title": "Bug1", "description": "desc", "priority": "low"},
                headers={"Authorization": f"Bearer {token}"})
    client.post("/tickets", json={"title": "Bug2", "description": "desc", "priority": "high"},
                headers={"Authorization": f"Bearer {token}"})
    # Filter by priority
    resp = client.get("/tickets?priority=high", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data["tickets"]) == 1
    assert data["tickets"][0]["title"] == "Bug2"
