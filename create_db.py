# appディレクトリの__init__.pyからdbをimport
from app import db

# データベースを作成するためのコード。pythonコンソールで行うことが多いですが面倒臭いのでターミナルから実行できるようにしました。
db.create_all()