import json
import os
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import requests
from requests.exceptions import RequestException
import time
import logging
from config import get_config
from cachetools import TTLCache
from functools import wraps  # Add this line

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Constants
CACHE_DURATION = 60  # seconds
RATE_LIMIT = 50  # requests
RATE_LIMIT_PERIOD = 60  # seconds
FALLBACK_DATA_FILE = 'fallback_crypto_data.json'

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(get_config())
socketio = SocketIO(app)

# Cache setup
cache = TTLCache(maxsize=100, ttl=CACHE_DURATION)

# Rate limiting setup
request_count = 0
last_reset = time.time()

def rate_limited(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        global request_count, last_reset
        current_time = time.time()
        
        if current_time - last_reset > RATE_LIMIT_PERIOD:
            request_count = 0
            last_reset = current_time
        
        if request_count >= RATE_LIMIT:
            return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
        
        request_count += 1
        return f(*args, **kwargs)
    return decorated_function

# Use Flask's app context to store selected_coins
app.config['SELECTED_COINS'] = ['bitcoin', 'ethereum']  # Default coins

# Fallback data functions
def load_fallback_data():
    try:
        with open(FALLBACK_DATA_FILE, 'r') as f:
            data = json.load(f)
        logger.info(f"Loaded fallback data for {len(data)} coins")
        return data
    except FileNotFoundError:
        logger.warning(f"Fallback data file not found: {FALLBACK_DATA_FILE}")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Error decoding fallback data file: {FALLBACK_DATA_FILE}")
        return {}

fallback_data = load_fallback_data()

def get_coins_data(coin_ids):
    cache_key = ','.join(sorted(coin_ids))
    if cache_key in cache:
        logger.info(f"Returning cached data for {cache_key}")
        return cache[cache_key], False  # Return cached data and is_stale=False

    logger.info(f"Fetching fresh data for {coin_ids}")
    try:
        ids = ','.join(coin_ids)
        url = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={ids}&order=market_cap_desc&per_page=250&page=1&sparkline=false'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        formatted_data = []
        for coin in data:
            formatted_data.append({
                'id': coin['id'],
                'name': coin['name'],
                'symbol': coin['symbol'],
                'current_price': coin['current_price'],
                'price_change_percentage_24h': coin['price_change_percentage_24h'],
                'market_cap': coin['market_cap'],
                'volume_24h': coin['total_volume']
            })
        
        logger.info(f"Caching and returning fresh data for {cache_key}")
        cache[cache_key] = formatted_data
        return formatted_data, False  # Return fresh data and is_stale=False
    except Exception as e:
        logger.error(f"Error fetching coin data: {e}")
        return [], True  # Return empty list and is_stale=True in case of error

@app.route('/')
def dashboard():
    coins_data, _ = get_coins_data(app.config['SELECTED_COINS'])
    return render_template('dashboard.html', coins=coins_data)

@app.route('/get_all_coins')
@rate_limited
def get_all_coins():
    try:
        url = 'https://api.coingecko.com/api/v3/coins/markets'
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 250,
            'page': 1,
            'sparkline': False
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        coins = response.json()
        result = [{'id': coin['id'], 'symbol': coin['symbol'], 'name': coin['name']} for coin in coins]
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error fetching all coins: {e}")
        return jsonify({'error': 'Failed to fetch coins'}), 500

# Add this new global variable
TOP_COINS = []
LAST_TOP_COINS_UPDATE = 0
TOP_COINS_UPDATE_INTERVAL = 24 * 60 * 60  # 24 hours in seconds

def update_top_coins():
    global TOP_COINS, LAST_TOP_COINS_UPDATE
    current_time = time.time()
    if current_time - LAST_TOP_COINS_UPDATE > TOP_COINS_UPDATE_INTERVAL:
        try:
            url = 'https://api.coingecko.com/api/v3/coins/markets'
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 20,
                'page': 1,
                'sparkline': False
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            coins = response.json()
            TOP_COINS = [{'id': coin['id'], 'symbol': coin['symbol'], 'name': coin['name']} for coin in coins]
            LAST_TOP_COINS_UPDATE = current_time
            logger.info("Updated top coins list")
        except Exception as e:
            logger.error(f"Error updating top coins: {e}")

# Call this function when the app starts
update_top_coins()

@app.route('/get_top_coins')
def get_top_coins():
    update_top_coins()  # This will only update if necessary
    return jsonify(TOP_COINS)

@socketio.on('connect')
def handle_connect():
    logger.info('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    logger.info('Client disconnected')

@socketio.on('update_selected_coins')
def handle_update_selected_coins(new_selected_coins):
    logger.info(f"Updating selected coins: {new_selected_coins}")
    app.config['SELECTED_COINS'] = new_selected_coins
    coins_data, is_stale = get_coins_data(new_selected_coins)
    emit('update_crypto_data', {'data': coins_data, 'is_stale': is_stale})

def background_task():
    logger.info("Background task started")
    while True:
        logger.info("Fetching new data in background task")
        coins_data, is_stale = get_coins_data(app.config['SELECTED_COINS'])
        logger.info(f"Emitting update for {len(coins_data)} coins, stale: {is_stale}")
        socketio.emit('update_crypto_data', {'data': coins_data, 'is_stale': is_stale})
        time.sleep(60)  # Update every 60 seconds

if __name__ == '__main__':
    from threading import Thread
    Thread(target=background_task, daemon=True).start()
    socketio.run(app, debug=True)