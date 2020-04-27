from flask import request, redirect, url_for, render_template, flash, session
from app import HOUSEHOLD
from app import db
from app.views.entries import Entry

@app.route('add')
def show_entries():
  if not session.get('logged_in'):
    return redirect(url_for('index'))
  entries = Entry.query.order_by(Entry.id.desc()).all()
  return render_template('index.html', entries=entries)