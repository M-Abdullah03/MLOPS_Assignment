import json
from src.app import app
import pytest


@pytest.fixture
def client():
    """Create a test client for the app."""
    app.testing = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """Test that home page renders correctly."""
    response = client.get('/')
    assert response.status_code == 200


def test_predict_json_input(client):
    """Test prediction with JSON input."""
    # Use real prediction instead of mocking
    response = client.post(
        '/predict',
        data=json.dumps({'input': '1, 2016-01-01 12:00:00'}),
        content_type='application/json'
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    # Check for the expected structure
    assert 'region_id' in data
    assert 'time' in data
    assert 'time_slot' in data
    assert 'prediction' in data
    assert data['region_id'] == 1
    # We don't assert exact values for time and prediction since they depend on the actual model


def test_predict_form_input(client):
    """Test prediction with form input."""
    response = client.post(
        '/predict',
        data={'input': '2, 2016-01-01 15:30:00'}
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    # Check for the expected structure
    assert 'region_id' in data
    assert 'time' in data
    assert 'time_slot' in data
    assert 'prediction' in data
    assert data['region_id'] == 2
    # We don't assert exact values for time and prediction since they depend on the actual model


def test_predict_missing_input(client):
    """Test prediction with missing input."""
    response = client.post('/predict', data={})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data == {'error': 'No input provided'}


def test_predict_invalid_input(client):
    """Test prediction with invalid input format."""
    response = client.post(
        '/predict',
        data={'input': 'invalid format'}
    )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert data == {'error': 'Invalid input format. Expected format: "region_id, YYYY-MM-DD HH:MM:SS"'}
