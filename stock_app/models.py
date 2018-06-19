from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from stock_app import db
from stock_app import login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), index=True, unique=True)
    vendor_code = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String, index=False, unique=False)
    price = db.Column(db.Integer, index=True, unique=False)
    amount = db.Column(db.Integer, index=True, unique=False)

    def __repr__(self):
        return '<Item {} {}>'.format(self.vendor_code, self.uuid)
