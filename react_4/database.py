
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite DB を作成
DATABASE_URL = "sqlite:///./test.db"

# DB 接続用エンジン
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# セッション作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデル定義ベース
Base = declarative_base()

# モデル定義
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)