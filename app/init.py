from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pushjack import FlaskPushJack

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
push_manager = FlaskPushJack(app)

from app import routes, models, forms, service_worker, push_notifications