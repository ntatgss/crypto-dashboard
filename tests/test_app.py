import sys
import os

# Get the absolute path of the current file (test_app.py)
current_file_path = os.path.abspath(__file__)

# Get the directory containing test_app.py (the tests folder)
tests_dir = os.path.dirname(current_file_path)

# Get the parent directory of the tests folder (project root)
project_root = os.path.dirname(tests_dir)

# Add the project root to the Python path
sys.path.insert(0, project_root)

# Now try to import create_app and Config
from first import create_app
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory database for testing

def create_test_app():
    return create_app(TestConfig)

# Don't create the app here, just provide the function