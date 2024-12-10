import os

SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

PUSHJACK_ACCESS_TOKEN = os.environ.get('PUSHJACK_ACCESS_TOKEN')
PUSHJACK_SECRET_KEY = os.environ.get('PUSHJACK_SECRET_KEY')