from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from . import db, socketio
from . import main
from .models import User
from .forms import LoginForm, RegistrationForm
from .user_settings import get_user_coins, update_user_coins
from .decorators import rate_limited
import time
import requests
import logging
from threading import Thread

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)

# Add these global variables
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

def get_coins_data(coin_ids):
    # Implement this function to fetch data for the given coin IDs
    # Return the fetched data and a boolean indicating if the data is stale
    pass

def background_task():
    logger.info("Background task started")
    while True:
        logger.info("Fetching new data in background task")
        coins_data, is_stale = get_coins_data(User.query.all())
        logger.info(f"Emitting update for {len(coins_data)} coins, stale: {is_stale}")
        socketio.emit('update_crypto_data', {'data': coins_data, 'is_stale': is_stale}, namespace='/')
        time.sleep(60)  # Update every 60 seconds

@main.route('/')
@login_required
@rate_limited(60)  # Adjust the number as needed
def index():
    return render_template('index.html')

@main.route('/get_top_coins')
def get_top_coins():
    update_top_coins()  # This will only update if necessary
    return jsonify(TOP_COINS)

# Add other routes here...

@socketio.on('connect')
def handle_connect():
    if not current_user.is_authenticated:
        return False
    else:
        socketio.emit('connection_response', {'data': 'Connected'})

@socketio.on('disconnect')
def handle_disconnect():
    logger.info('Client disconnected')

@socketio.on('update_selected_coins')
def handle_update_selected_coins(new_selected_coins):
    if current_user.is_authenticated:
        logger.info(f"Updating selected coins for user {current_user.id}: {new_selected_coins}")
        update_user_coins(current_user, new_selected_coins)
        coins_data, is_stale = get_coins_data(new_selected_coins)
        socketio.emit('update_crypto_data', {'data': coins_data, 'is_stale': is_stale})
    else:
        logger.warning("Unauthenticated user tried to update selected coins")
        socketio.emit('error', {'message': 'Authentication required'})

# Call this function when the app starts
update_top_coins()

# Remove this line from the bottom of the file:
# Thread(target=background_task).start()

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)
