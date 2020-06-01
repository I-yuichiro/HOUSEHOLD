from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.services import auth_service
from app import db
from app.models.entries import Entry


auth = Blueprint('auth', __name__)

# signupページと、postするページを共通化
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'GET':
    return render_template('auth/signup.html')
  else:
    user = auth_service.signup(request.form)
    if user:
      flash('メールアドレスはすでに登録されています。')
      return redirect(url_for('layout'))
    flash('新規登録に成功しました。')
    return redirect(url_for('auth.index'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('/auth/login.html')
  else:
    user = auth_service.login(request.form)
    if not user:
      flash('メールアドレスもしくはパスワードに誤りがあります。')
      return render_template('/auth/login.html')
    flash('ログインしました。')
    session['logged_in'] = True
    return redirect('/index')

@auth.route('/logout')
@login_required
def logout():
  auth_service.logout()
  flash('ログアウトしました。')
  return redirect(url_for('auth.login'))

#?
@auth.route('/index', methods=['GET','POST'])
def index():
  if not session.get('logged_in'):
    return redirect('/auth/login.html')
  else:
    entries = Entry.query.all()
  return render_template('/index.html',entries=entries) 

#?
@auth.route('/add')
def add():
  return render_template('/auth/add.html')

@auth.route('/add', methods=['GET', 'POST'])
def add_entry():
  if not session.get('logged_in'):
    return redirect(url_for('index'))
  entries = Entry(
    categories = request.form['categories'],
    cost = request.form['cost']
  )
  print(request.form['categories'])
  db.session.add(entries)
  db.session.commit()
  return redirect(url_for('index'))