from .models import User
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from grocery_app.config import Config
import os
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)
# Create a LoginManager instance

login_manager = LoginManager()

# Set the login view to auth.login

login_manager.login_view = 'auth.login'

# initialize it with the app

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


bcrypt = Bcrypt(app)
