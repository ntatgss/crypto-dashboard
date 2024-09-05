import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask configuration
    DEBUG = False

    # API configuration
    COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
    
    # Rate limiting
    RATE_LIMIT = 50  # requests
    RATE_LIMIT_PERIOD = 60  # seconds

    # Caching
    CACHE_DURATION = 60  # seconds

    # Coins to track
    TRACKED_COINS = ['bitcoin', 'ethereum', 'binancecoin', 'ripple', 'cardano']
    
    # Fallback data
    FALLBACK_DATA_FILE = 'fallback_crypto_data.json'

    # Background task configuration
    UPDATE_INTERVAL = 60  # seconds

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    # Production-specific settings
    pass

# You can add more configuration classes as needed

# Set the active configuration
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    return config[os.environ.get('FLASK_ENV') or 'default']
