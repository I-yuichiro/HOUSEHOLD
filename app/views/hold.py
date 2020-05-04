from flask import request, redirect, url_for, render_template, flash, session
from app import app
from app import db
from app.models.entries import Entry, entries


@app.route('/add', methods=['GET', 'POST'])
def add_entry():
  flash('新しい項目が追加されました。')
  return redirect(url_for('index'))

  entry = Entry(
    categories = request.form['categories'],
    cost = request.form['cost']
  )
  db.session.add(entry)
  db.session.commit()

  
