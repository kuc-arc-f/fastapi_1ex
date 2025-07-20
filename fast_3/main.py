from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

#from . import crud, models, schemas
#from .database import SessionLocal, engine, get_db
from mypack.crud import *
from mypack.database import SessionLocal, engine, get_db

# データベースのテーブルを（存在しなければ）作成する
#mypack.models.Base.metadata.create_all(bind=engine)
from mypack.schemas import Item, ItemCreate, ItemUpdate
from mypack.models import Base
Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- APIエンドポイント定義 ---
# 一覧表示機能 (Read All)
@app.get("/foo")
def read_foo(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return []

# 一覧表示機能 (Read All)
@app.get("/items/", response_model=List[Item], summary="アイテム一覧取得")
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

# 追加機能 (Create)
@app.post("/items", response_model=Item, status_code=201, summary="アイテム作成")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)

# 1件取得機能 (Read One)
@app.get("/items/{item_id}", response_model=Item, summary="単一アイテム取得")
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# 更新機能 (Update)
@app.put("/items/{item_id}", response_model=Item, summary="アイテム更新")
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_item(db, item_id=item_id, item_update=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# 削除機能 (Delete)
@app.delete("/items/{item_id}", response_model=Item, summary="アイテム削除")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
