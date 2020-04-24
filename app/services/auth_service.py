from flask_login import login_user, logout_user
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models.user import User

def signup(data: {}) -> User:
  try:
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
      return user

    new_user = User.from_args(name, email, password)

    db.session.add(new_user)
    db.session.commit()
    return user
  except SQLAlchemyError:
    raise SQLAlchemyError


def login(data: {}) -> User:
  try:
    email = data.get('email')
    password = data.get('password')
    remember = True if data.get('remember') else False
    user = User.query.filter_by(email=email).first()
    if not user and not user.check_password(user.password, password):
      raise SQLAlchemyError

    login_user(user, remember=remember)
    return user
  except SQLAlchemyError:
    raise SQLAlchemyError


def logout():
  logout_user()
  return True