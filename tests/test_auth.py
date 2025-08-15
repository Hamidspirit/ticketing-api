import json
import pytest
from ..app import create_app
from ..app.models import db

@pytest.fixture()
def client():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
    client = app.test_client()
    yield client
    with app.app_context():
        db.drop_all()

def test_register_and_login(client):
    # Register
    resp = client.post("/auth/register", json={"username": "alice", "password": "secret123"})
    assert resp.status_code == 201
    # Login
    resp = client.post("/auth/login", json={"username": "alice", "password": "secret123"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data
