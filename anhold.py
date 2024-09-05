from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from flask_caching import Cache
import requests
import time
import threading
import random

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
socketio = SocketIO(app)

def get_crypto_data(max_retries=3, initial_delay=1):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,  # Increased to get more coins
        "page": 1,
        "sparkline": False
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return {coin['symbol'].lower(): {'price': coin['current_price'], 'market_cap': coin['market_cap']} for coin in data}
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                delay = initial_delay * (2 ** attempt) + random.uniform(0, 1)
                print(f"Retrying in {delay:.2f} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Using fallback data.")
                return {
                    "btc": {"price": 50000, "market_cap": 1000000000000},
                    "eth": {"price": 3000, "market_cap": 500000000000},
                    "doge": {"price": 0.5, "market_cap": 50000000000},
                    "sol": {"price": 100, "market_cap": 20000000000},
                    "bnb": {"price": 300, "market_cap": 50000000000}
                }

@app.route('/')
def index():
    crypto_data = get_crypto_data()
    print("Crypto Data:", crypto_data)
    return render_template('dashboard.html', crypto_data=crypto_data)

def background_task():
    while True:
        try:
            crypto_data = get_crypto_data()
            print("Background task data:", crypto_data)
            socketio.emit('update_prices', crypto_data)
        except Exception as e:
            print(f"Error in background task: {e}")
        time.sleep(60)  # Update every 60 seconds instead of 10

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    threading.Thread(target=background_task, daemon=True).start()
    socketio.run(app, debug=True)