from app import db, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    username = db.Column(db.String(20), unique=True)
    bio = db.Column(db.String(240))
    email = db.Column(db.String(254), unique=True)
    tdr_title = db.Column(db.String(60))
    tdr_description = db.Column(db.String(500))
    tdr_subject = db.Column(db.String())
    tdr_year = db.Column(db.String())
    tdr_mark = db.Column(db.Integer)
    tdr_school = db.Column(db.String(120))
    password = db.Column(db.String(80))
    creation_date = db.Column(db.Date())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
