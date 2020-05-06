from app import db

class Entry(db.Model):
  __tablename__ = 'entries'
  categories = db.Column(db.Text)
  cost = db.Column(db.Integer, primary_key=True)

  def __init__(self, categories=None, cost=None):
    self.categories = categories
    self.cost = cost

  def __repr__(self):
    return '<Entry id:{} categories:{} cost:{}>'.format(self.cost, self.categories)