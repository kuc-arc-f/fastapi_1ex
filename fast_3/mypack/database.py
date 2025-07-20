import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

# autocommit=False: データを変更しても自動でコミットしない
# autoflush=False: session.add()などをしても自動でDBにSQLを発行しない
# bind=engine: このセッションがどのエンジンを使うかを指定
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルクラスが継承するためのBaseクラス
Base = declarative_base()

# APIがリクエストごとにDBセッションを取得するための依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()