from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from app.models.user import User

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

from app.views.auth import auth

app.register_blueprint(auth)

@app.route('/')
def layout():
  return render_template('layout.html')