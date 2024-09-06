# 1st/app_for_testing.py

import sys
import os

# Add the current directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Now we can import create_app
import __init__
from config import Config

app = __init__.create_app(Config)

if __name__ == '__main__':
    app.run(debug=True)