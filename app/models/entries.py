from app import db

class Entry(db.Model):
  __tablename__ = 'entries'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer)
  categories = db.Column(db.Text)
  cost = db.Column(db.Integer)

  def __init__(self, categories=None, cost=None, user_id=None):
    self.categories = categories
    self.cost = cost
    self.user_id = user_id
    self.all = all

    #なければテーブル作成
    db.create_all()

  def __repr__(self):
    return '<Entry all:{}>'.format(self.all)