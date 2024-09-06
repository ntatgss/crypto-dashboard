# tests/test_frontend.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from flask import session
from flask_login import login_user, current_user
import time
import threading
import sys
import os
from http.cookiejar import Cookie

# Get the absolute path of the current file (test_frontend.py)
current_file_path = os.path.abspath(__file__)

# Get the directory containing test_frontend.py (the tests folder)
tests_dir = os.path.dirname(current_file_path)

# Get the parent directory of the tests folder (project root)
project_root = os.path.dirname(tests_dir)

# Add the project root to the Python path
sys.path.insert(0, project_root)

# Now import necessary modules
from first import create_app, db
from first.models import User
from first.config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost:5000'
    SECRET_KEY = 'test-secret-key'
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    LOGIN_DISABLED = True  # Add this line to disable login requirements in test environment

@pytest.fixture(scope="module")
def flask_app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        # Create a test user
        test_user = User(username='testuser', email='test@example.com')
        test_user.set_password('testpassword')
        db.session.add(test_user)
        db.session.commit()
        print(f"Test user created: {test_user.username}, {test_user.email}")
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="module")
def client(flask_app):
    return flask_app.test_client()

@pytest.fixture(scope="module")
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def authenticated_driver(flask_app, driver, client):
    with flask_app.app_context():
        # Find the test user
        test_user = User.query.filter_by(username='testuser').first()
        print(f"Test user found: {test_user}")
        if not test_user:
            all_users = User.query.all()
            print(f"All users in database: {all_users}")
            pytest.fail("Test user not found. Make sure it's created in the database.")

        # Log in the user
        with client.session_transaction() as sess:
            sess['_user_id'] = str(test_user.id)

        # Verify login
        response = client.get('/dashboard')
        print(f"Dashboard response status: {response.status_code}")
        print(f"Dashboard response data: {response.data}")

        if response.status_code != 200 or b'Sign In' in response.data:
            pytest.fail("Failed to log in the test user")

        # Get the session cookie
        session_cookie = client.get_cookie('session')
        if not session_cookie:
            pytest.fail("No session cookie found after login")

        print(f"Session cookie: {session_cookie}")

    # Navigate to the home page first
    driver.get(f"http://{flask_app.config['SERVER_NAME']}")
    print(f"Home page URL: {driver.current_url}")

    # Add the session cookie to the Selenium driver
    driver.add_cookie({
        'name': 'session',
        'value': session_cookie.value,
        'path': '/',
        'domain': flask_app.config['SERVER_NAME'].split(':')[0],
        'secure': False,
        'httpOnly': True,
        'sameSite': 'Lax'
    })

    # Navigate to the dashboard
    dashboard_url = f"http://{flask_app.config['SERVER_NAME']}/dashboard"
    driver.get(dashboard_url)
    print(f"Dashboard URL: {driver.current_url}")
    print(f"Dashboard page source: {driver.page_source}")

    # Wait for the dashboard to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cryptoContainer"))
        )
        print("Successfully loaded dashboard")
    except Exception as e:
        print(f"Current URL after waiting: {driver.current_url}")
        print(f"Dashboard page source after waiting: {driver.page_source}")
        print(f"Exception details: {str(e)}")
        pytest.fail(f"Failed to load dashboard: {str(e)}")

    return driver

def test_refresh_crypto_data(authenticated_driver):
    try:
        # Wait for the refresh button to be clickable
        refresh_button = WebDriverWait(authenticated_driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Refresh Data') or @onclick='refreshCryptoData()']"))
        )
        refresh_button.click()
        
        # Wait for crypto cards to be present
        WebDriverWait(authenticated_driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "crypto-card"))
        )
    except Exception as e:
        print(f"Current URL: {authenticated_driver.current_url}")
        print(f"Page source: {authenticated_driver.page_source}")
        pytest.fail(f"Failed to refresh crypto data: {str(e)}")

    crypto_cards = authenticated_driver.find_elements(By.CLASS_NAME, "crypto-card")
    assert len(crypto_cards) > 0, "No crypto cards found after refresh"

def test_dark_mode_toggle(authenticated_driver, flask_app):
    try:
        # Wait for the toggle to be clickable
        toggle = WebDriverWait(authenticated_driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".theme-switch input[type='checkbox']"))
        )
        toggle.click()
        
        # Wait for the body to have the dark-mode class
        WebDriverWait(authenticated_driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body.dark-mode"))
        )
    except Exception as e:
        print(f"Current URL: {authenticated_driver.current_url}")
        print(f"Page source: {authenticated_driver.page_source}")
        pytest.fail(f"Failed to toggle dark mode: {str(e)}")

    body = authenticated_driver.find_element(By.TAG_NAME, "body")
    assert "dark-mode" in body.get_attribute("class"), "Dark mode not activated after toggle"

def test_dashboard_accessible(client):
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Crypto Dashboard' in response.data

def test_user_authentication(client):
    with client.session_transaction() as sess:
        sess['_user_id'] = '1'  # Assuming the test user has id 1
    
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Sign In' not in response.data
    assert b'Crypto Dashboard' in response.data

def test_user_authentication(authenticated_driver):
    # Check if the dashboard is accessible
    assert "Crypto Dashboard" in authenticated_driver.page_source
    
    # Check if the logout link is present (indicating the user is logged in)
    logout_link = authenticated_driver.find_elements(By.LINK_TEXT, "Logout")
    assert len(logout_link) > 0, "Logout link not found, user might not be authenticated"