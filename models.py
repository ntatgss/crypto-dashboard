from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    favorite_coins = db.Column(db.String(500), default='')  # Initialize with an empty string

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_favorite_coins(self):
        return self.favorite_coins.split(',') if self.favorite_coins else []

    def set_favorite_coins(self, coins):
        self.favorite_coins = ','.join(coins)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))