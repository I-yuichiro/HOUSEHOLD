from flask import request, redirect, url_for, render_template, flash, session
from HOUSEHOLD import app
from app import db
from app.views.entries import Entry

@app.route('')
def show_entries():
  if not session.get('logged_in'):
    return redirect(url_for('index'))
  entry = Entry.query.get(id)
  return render_template('/auth/add.html', entry=entry)