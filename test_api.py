import pytest
from fastapi.testclient import TestClient

# Import your router
from punto_2_main import app
from app.database.utils import load_initial_data

# Define the authentication headers
headers = {}


@pytest.fixture(scope="module")
def client():
    # Create a test client using the FastAPI app
    with TestClient(app) as client:
        # Load initial data to database if not exists

        # Get the authentication token
        response = client.post(
            "/api/auth/token",
            data={"username": "admin@mail.com", "password": "pass123"},
        )
        assert response.status_code == 200
        token = response.json()["access_token"]
        headers["Authorization"] = f"Bearer {token}"
        yield client


def test_get_participants(client):
    # Test the GET /api/participants endpoint with authentication
    response = client.get("/api/participants", headers=headers)
    assert response.status_code == 200
    participants = response.json()
    assert isinstance(participants, list)


def test_get_participant(client):
    # Test the GET /api/participants/{participant_id} endpoint with authentication
    participant_id = 1
    response = client.get(f"/api/participants/{participant_id}", headers=headers)
    assert response.status_code == 200
    participant = response.json()
    assert participant["id"] == participant_id


def test_get_processes(client):
    # Test the GET /api/processes endpoint with authentication
    response = client.get("/api/processes", headers=headers)
    assert response.status_code == 200
    processes = response.json()
    assert isinstance(processes, list)


def test_get_process(client):
    # Test the GET /api/processes/{process_id} endpoint with authentication
    process_id = 1
    response = client.get(f"/api/processes/{process_id}", headers=headers)
    assert response.status_code == 200
    process = response.json()
    assert process["id"] == process_id


def test_get_process_details(client):
    # Test the GET /api/process-details endpoint with authentication
    response = client.get("/api/process-details", headers=headers)
    assert response.status_code == 200
    process_details = response.json()
    assert isinstance(process_details, list)


def test_get_process_detail(client):
    # Test the GET /api/process-details/{process_detail_id} endpoint with authentication
    process_detail_id = 1
    response = client.get(f"/api/process-details/{process_detail_id}", headers=headers)
    assert response.status_code == 200
    process_detail = response.json()
    assert process_detail["id"] == process_detail_id


def test_get_proceedings(client):
    # Test the GET /api/process-details/{process_detail_id}/proceedings endpoint with authentication
    process_detail_id = 1
    response = client.get(
        f"/api/process-details/{process_detail_id}/proceedings",
        headers=headers,
    )
    assert response.status_code == 200
    proceedings = response.json()
    assert isinstance(proceedings, list)


if __name__ == "__main__":
    pytest.main()
