import pytest
from app.api.api import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_create_account(client):
    response = client.post("/create_account", json={"owner": "Alice"})
    assert response.status_code == 201
    assert response.get_json()["message"] == "Account created successfully"


def test_create_duplicate_account(client):
    client.post("/create_account", json={"owner": "Alice"})  # Create once
    response = client.post("/create_account", json={"owner": "Alice"})  # Try to create again
    assert response.status_code == 400
    assert response.get_json()["message"] == "Account already exists"


def test_deposit(client):
    client.post("/create_account", json={"owner": "Bob"})
    response = client.post("/deposit", json={"owner": "Bob", "amount": 100})
    assert response.status_code == 200
    assert response.get_json()["balance"] == 100


def test_withdraw_success(client):
    client.post("/create_account", json={"owner": "Charlie"})
    client.post("/deposit", json={"owner": "Charlie", "amount": 200})
    response = client.post("/withdraw", json={"owner": "Charlie", "amount": 100})
    assert response.status_code == 200
    assert response.get_json()["balance"] == 100


def test_withdraw_insufficient_funds(client):
    client.post("/create_account", json={"owner": "Dave"})
    client.post("/deposit", json={"owner": "Dave", "amount": 50})
    response = client.post("/withdraw", json={"owner": "Dave", "amount": 100})
    assert response.status_code == 200
    assert response.get_json()["balance"] == "Insufficient funds"


def test_withdraw_nonexistent_account(client):
    response = client.post("/withdraw", json={"owner": "Eve", "amount": 50})
    assert response.status_code == 404
    assert response.get_json()["message"] == "Account not found"


def test_deposit_nonexistent_account(client):
    response = client.post("/deposit", json={"owner": "Frank", "amount": 50})
    assert response.status_code == 404
    assert response.get_json()["message"] == "Account not found"


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode() == "Welcome to the Bank API"
