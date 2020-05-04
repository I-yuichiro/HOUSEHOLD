from app import db
from datetime import datetime

class Entry(db.Model):
  __tablename__ = 'entries'
  categories = db.Column(db.Text)
  cost = db.Column(db.Integer, primary_key=True)

  @classmethod
  def from_args(cls, categories: str, cost: str):
    instance = cls()
    instance.categories = categories
    instance.cost = cost
    return instance