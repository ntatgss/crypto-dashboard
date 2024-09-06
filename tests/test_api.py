# tests/test_api.py

import pytest
from tests.test_app import create_test_app
from first.models import User, db

@pytest.fixture
def app():
    app = create_test_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_crypto_data(client):
    response = client.get('/get_crypto_data?coins=bitcoin,ethereum')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert 'bitcoin' in [coin['id'] for coin in data]
    assert 'ethereum' in [coin['id'] for coin in data]

def test_get_top_coins(client):
    response = client.get('/get_top_coins')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 100  # Assuming you're fetching top 100 coins

# Add more tests for other API endpoints