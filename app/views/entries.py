from flask import request, redirect, url_for, render_template, flash, session
from app import app
from app import db
from app.models.entries import Entry

@app.route('index.html')
def show_entries():
  if not session.get('logged_in'):
    return redirect(url_for('add.html'))
  entries = Entry.query.order_by(Entry.id.desc()).all()
  return render_template('index.html', entries=entries)

@app.route('/auth.add.html', methods=['POST'])
def add_entry():
  if not session.get('logged_in'):
    return redirect(url_for('index.html'))
  entry = Entry(
    追加 = request.form['追加'],
    編集 = request.form['編集'],
    削除 = request.form['削除']
  )
db.session.add(entry)
db.session.commit()
return redirect(url_for('show_entries'))

