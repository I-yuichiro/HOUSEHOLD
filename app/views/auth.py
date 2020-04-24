from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required

from app.services import auth_service

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'GET':
    return render_template('auth/signup.html')
  else:
    user = auth_service.signup(request.form)
    if user:
      flash('メールアドレスはすでに登録されています。')
      return redirect(url_for('index'))
    flash('新規登録に成功しました。')
    return redirect(url_for('index'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('auth/login.html')
  else:
    user = auth_service.login(request.form)
    if not user:
      flash('メールアドレスもしくはパスワードに誤りがあります。')
      return render_template('auth.login')
    flash('ログインしました。')
    return redirect(url_for('index'))


@auth.route('/logout')
@login_required
def logout():
  auth_service.logout()
  flash('ログアウトしました。')
  return redirect(url_for('auth.login'))