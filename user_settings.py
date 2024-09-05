from .models import db, User

def get_user_coins(user):
    return user.selected_coins.split(',') if user.selected_coins else ['bitcoin', 'ethereum']

def update_user_coins(user, coins):
    user.selected_coins = ','.join(coins)
    db.session.commit()