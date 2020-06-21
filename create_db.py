# appディレクトリの__init__.pyからdbをimport
from app import db

# データベースを作成するためのコード
db.create_all()