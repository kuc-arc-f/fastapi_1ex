from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from typing import List

# SQLAlchemy関連のインポート
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Pydanticモデル（スキーマ）のインポート
from pydantic import BaseModel

# --- データベース設定 ---

# 1. SQLiteデータベースのURLを定義
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# 2. SQLAlchemyのエンジンを作成
# connect_argsはSQLiteでのみ必要です
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. データベースセッションを作成するためのSessionLocalクラスを定義
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. モデルクラスが継承するBaseクラスを定義
Base = declarative_base()


# --- SQLAlchemyモデル（データベースのテーブル定義） ---

class Item(Base):
    __tablename__ = "items"  # テーブル名

    # テーブルの項目（カラム）を定義
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, index=True)


# --- Pydanticモデル（APIのスキーマ定義） ---
# APIが受け取ったり返したりするデータの形を定義します

# 共通のベースモデル
class ItemBase(BaseModel):
    name: str

# データ作成時に使用するモデル
class ItemCreate(ItemBase):
    pass

# データを読み取る時に使用するモデル（レスポンスモデル）
class ItemResponse(ItemBase):
    id: int

    # SQLAlchemyモデルからPydanticモデルへ変換できるように設定
    class Config:
        orm_mode = True


# --- FastAPIアプリケーションの初期化 ---

app = FastAPI()

# public フォルダを静的ファイルとしてマウント
# /static というURLパスで public フォルダの内容にアクセスできるようになります。
app.mount("/static", StaticFiles(directory="public"), name="static")

# Jinja2Templates を使用してHTMLテンプレートをレンダリングする場合
# templates フォルダにHTMLファイルがあることを想定
templates = Jinja2Templates(directory="templates")

# データベースのテーブルを初期化（もし存在しなければ作成）
Base.metadata.create_all(bind=engine)


# --- データベースセッションの依存関係 ---
# APIエンドポイント内でデータベースセッションを取得するための関数

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- APIエンドポイント（CRUD処理） ---

# POST-Test
@app.post("/post_test")
def post_text_api(item: ItemCreate):
    return "OK"

# C: Create (作成機能)
@app.post("/items", response_model=ItemResponse, summary="項目の追加")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """
    新しい項目をデータベースに追加します。
    - **name**: 項目の名前 (TEXT型)
    """
    db_item = Item(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# R: Read (一覧表示機能)
@app.get("/items", response_model=List[ItemResponse], summary="項目の一覧表示")
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    データベース内のすべての項目を一覧で取得します。
    - **skip**: スキップする項目数
    - **limit**: 取得する最大項目数
    """
    items = db.query(Item).offset(skip).limit(limit).all()
    return items

# U: Update (更新機能)
@app.put("/items/{item_id}", response_model=ItemResponse, summary="項目の更新")
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    """
    指定されたIDの項目を更新します。
    - **item_id**: 更新する項目のID
    - **name**: 新しい項目の名前
    """
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db_item.name = item.name
    db.commit()
    db.refresh(db_item)
    return db_item

# D: Delete (削除機能)
@app.delete("/items/{item_id}", response_model=ItemResponse, summary="項目の削除")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    指定されたIDの項目を削除します。
    - **item_id**: 削除する項目のID
    """
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return db_item

@app.get("/foo", response_class=HTMLResponse)
async def read_foo():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI Static Files</title>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    </head>
    <body>
        <div id="app"></div>
        <script type="module" src="/static/client.js"></script>
    </body>
    </html>
    """

@app.get("/bar")
def read_bar():
    return {"bar": "bar-2"}
