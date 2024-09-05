from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
import requests
from requests.exceptions import RequestException
import time

main = Blueprint('main', __name__)

def fetch_crypto_data(selected_coins, max_retries=3, delay=1):
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'ids': ','.join(selected_coins),
        'order': 'market_cap_desc',
        'per_page': 250,
        'page': 1,
        'sparkline': False,
        'price_change_percentage': '24h'
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                raise
            time.sleep(delay * (attempt + 1))  # Exponential backoff

    raise Exception("Failed to fetch crypto data after multiple attempts")

@main.route('/')
@login_required
def index():
    return render_template('dashboard.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main.route('/get_crypto_data')
@login_required
def get_crypto_data():
    selected_coins = request.args.get('coins', 'bitcoin,ethereum').split(',')
    
    print(f"Fetching data for coins: {', '.join(selected_coins)}")
    
    try:
        coins = fetch_crypto_data(selected_coins)
        print(f"Fetched data for {len(coins)} coins: {', '.join([coin['id'] for coin in coins])}")
        return jsonify(coins)
    except Exception as e:
        print(f"Error fetching crypto data: {str(e)}")
        return jsonify({"error": "Failed to fetch crypto data. Please try again later."}), 500

@main.route('/get_top_coins')
@login_required
def get_top_coins():
    # Fetch top 100 coins for the settings modal
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 100,
        'page': 1,
        'sparkline': False
    }
    response = requests.get(url, params=params)
    top_coins = response.json()
    return jsonify(top_coins)

@main.route('/update_selected_coins', methods=['POST'])
@login_required
def update_selected_coins():
    selected_coins = request.json
    # Here you can save the selected coins to the user's profile if needed
    return jsonify({'status': 'success'})