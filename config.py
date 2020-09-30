import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = 'YOUR_RANDOM_SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'bot.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

ACCESS_TOKEN = "EAAJdkh8NlycBAAyyeFC5uC7hPzrTZAQKh0uNDjXKVwI5pFYYZAVUcy6TS1Z"\
               "AjzPyyDmwgdHr2yIMcme3ZBfTv3ZA5ZBrZBmBtLyP7XKRgMlV9Io9euWrhX9"\
               "RKaZBbX25RoowLtJOmj1KTXs5mvglzkIIso3ZCH29RZAahSi3xUBoINDQZDZD"
VERIFY_TOKEN = "bot"
