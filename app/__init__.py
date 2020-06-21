#モジュールインポート
from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
from werkzeug.security import generate_password_hash, check_password_hash

# Flaskアプリの生成
app = Flask(__name__)

# ここから /// データベースの設定
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# sqlalchemyを通してflaskからdbアクセスをするための入り口
db = SQLAlchemy(app)

# flask-loginに関する設定
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# データベースのimport
from app.models.user import User

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

# authに関するルーティングを追加
from app.views.auth import auth

# authに関するルートをflaskアプリであるappに追加
app.register_blueprint(auth)

# 起動した際、layout.htmlのページに飛ぶ
@app.route('/')
def layout():
  return render_template('layout.html')