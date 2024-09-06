# tests/test_backend_functions.py

import pytest
from first import create_app, db
from first.models import User
from first.user_settings import get_user_coins, update_user_coins
from first.config import Config
import socketio
import time

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost:5000'

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_user_coins(app):
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.selected_coins = 'bitcoin,ethereum'
        assert get_user_coins(user) == ['bitcoin', 'ethereum']

def test_update_user_coins(app):
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        update_user_coins(user, ['bitcoin', 'dogecoin'])
        assert user.favorite_coins == 'bitcoin,dogecoin'

def test_home_page(client):
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome to Crypto Dashboard" in response.data or b"Login" in response.data

def test_dashboard_redirect_if_not_logged_in(client):
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data

def test_user_registration(client):
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'testpassword',
        'password2': 'testpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data  # Assuming it redirects to login page after registration

def test_user_login_logout(client, app):
    # Register a user
    client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
        'password2': 'testpassword'
    })

    # Login
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Dashboard" in response.data

    # Logout
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data  # Assuming it redirects to login page after logout

def test_get_crypto_data(client, app):
    with app.app_context():
        # Create and login a user
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        })

        # Test getting crypto data
        response = client.get('/get_crypto_data?coins=bitcoin,ethereum')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert any(coin['id'] == 'bitcoin' for coin in data)
        assert any(coin['id'] == 'ethereum' for coin in data)

def test_update_user_settings(client, app):
    with app.app_context():
        # Create and login a user
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpassword')
        user.selected_coins = 'bitcoin,ethereum'  # Set initial selected coins
        db.session.add(user)
        db.session.commit()

        response = client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        assert response.status_code == 302  # Redirect after successful login

        # Test the test route
        response = client.get('/test')
        assert response.status_code == 200
        assert response.data == b"Test route works!"

        # Test updating user settings via HTTP POST
        response = client.post('/update_settings', json={
            'selectedCoins': ['bitcoin', 'dogecoin']
        })
        assert response.status_code == 200
        assert response.get_json()['message'] == 'Settings updated successfully'

        # Verify the user's coins were updated
        updated_user = User.query.filter_by(username='testuser').first()
        assert set(updated_user.get_selected_coins()) == set(['bitcoin', 'dogecoin'])

# Add more tests for other backend functions as needed