import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_required_error'
login_manager.login_message = "Has d'iniciar sessió per poder accedir a aquesta pàgina."

from views import *


if __name__ == '__main__':
    app.run()
