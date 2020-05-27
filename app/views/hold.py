from flask import request, redirect, url_for, render_template, flash, session
from app import app
from app import db
from app.models.entries import Entry

@app.route('/add')
def show_entries():
  if not session.get('logged_in'):
    return redirect(url_for('login'))
  entries = Entry.query.order_by(Entry.id.desc()).all()
  return render_template('/index.html', entries=entries) 


@app.route('/add', methods=['GET', 'POST'])
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


@app.route('/index/<int:id>', methods=["GET"])
def show_entry(id):
  if not session.get('logged_in'):
    return redirect(url_for('add'))
  entry = Entry.query.get(id)
  return render_template('index.html', entry=entry)

  
