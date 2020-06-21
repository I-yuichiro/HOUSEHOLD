from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.views import auth_service
from app import db
from app.models.entries import Entry
import random

auth = Blueprint('auth', __name__)

# signupページと、postするページを共通化
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'GET':
    return render_template('/signup.html')
  else:
    user = auth_service.signup(request.form)
    if user:
      flash('メールアドレスはすでに登録されています')
      return redirect(url_for('layout'))
    flash('新規登録に成功しました')
    return redirect('/login')

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('/login.html')
  else:
    user = auth_service.login(request.form)
    if not user:
      flash('メールアドレスもしくはパスワードに誤りがあります')
      return render_template('/login.html')
    session['user_id'] = user.id
    flash('ログインしました')
    return redirect('/index')


@auth.route('/index', methods=['GET','POST'])
def index():
  # 表示するリスト
  entries = []
  # entries += [{'categroies': "初期値", 'cost': 0, 'per': 100}]
  # print(str(request.method)) 

  # from /add
  if request.method == 'POST' and 'title' in request.form and 'cost' in request.form:
    # ポストされる内容
    # print(str(request.form["title"]))
    # print(str(request.form["cost"]))

    #項目が入っていなかったときの処理
    if 1 > len(request.form["title"]) or 1 > len(request.form["cost"]):
      flash('項目、数字入力してください')
      return redirect('/index')

    # 送られた内容を保存
    add_cat = str(request.form["title"])
    add_cost= int(request.form["cost"])

    record = Entry(add_cat,add_cost,session['user_id'])
    flash('項目追加されました')
    db.session.add(record)
    db.session.commit()

    entries += [{'categroies':add_cat,'cost':add_cost,'per': 100}]
    # リロードされた時再度ここに入らない対策
    return redirect('/index')

  # 保存されたレコードを取得
  res = Entry.query.filter(Entry.user_id == session['user_id'])

  # 合計値を取得
  csum = 0
  for r in res:
    csum += r.cost

  # # print(type(res))
  for r in res:
    # print(str(r.id))
    per = '{:.1f}'.format(r.cost/csum*100)
    entries += [{'categroies':r.categories,'cost':r.cost,'per': per, 'id': r.id}]
  # # print(str(entries))
  
  # レンダリング（表示）
  return render_template('/index.html', entries=entries) 


# index.htmlからadd.htmlに行く処理
@auth.route('/add')
def add():
  return render_template('/add.html')

# 編集画面を押したら編集画面に返す
@auth.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_entry(id):
  entry = Entry.query.filter(Entry.id == id).first()
  return render_template('edit.html',entry=entry)


#編集内容を受け取りデータベースを更新する処理
@auth.route('/<int:id>/update', methods=['POST'])
def update_entry(id):
  print("update_entry")
  add_cat = str(request.form["title"])
  add_cost= int(request.form["cost"])
  entry = Entry.query.filter(Entry.id == id).first()
  entry.categories = add_cat
  entry.cost = add_cost
  db.session.add(entry)
  db.session.commit()
  flash('更新されました')
  return redirect(url_for('auth.index'))

#項目を削除
@auth.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_entry(id):
  entry = Entry.query.filter(Entry.id == id).first()
  db.session.delete(entry)
  db.session.commit()
  flash('削除されました')
  return redirect(url_for('auth.index'))

# index.htmlからpie.htmlに行く処理
@auth.route('/pie')
def pie():
  entries = []
  res = Entry.query.filter()

  csum = 0
  for r in res:
    csum += r.cost

  for r in res:
    per = '{:.1f}'.format(r.cost/csum*100)
    entries += [{'categroies':r.categories,'cost':r.cost, 'per': per}]

  g = []
  d = []
  c = []
  for entry in entries:
    g += [entry['categroies']]
    d += [entry['cost']]

    tc = "#"+ str(hex(random.randint(0, 255))[2:]).zfill(2) \
            + str(hex(random.randint(0, 255))[2:]).zfill(2) \
            + str(hex(random.randint(0, 255))[2:]).zfill(2)

    print(tc)
    c.append(tc)

  return render_template('/pie.html', entries=entries,g=g,d=d,c=c)


@auth.route('/logout')
@login_required
def logout():
  auth_service.logout()
  flash('ログアウトしました')
  return redirect(url_for('auth.login'))