import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

WTF_CSRF_ENABLED = True
SECRET_KEY = 'secret'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAX_CONTENT_LENGTH = 100 * 1024 * 1024
