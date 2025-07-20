from sqlalchemy.orm import Session
from .. import models, schemas

def get_item(db: Session, item_id: int):
    """IDでアイテムを1件取得"""
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    """アイテムを複数件取得"""
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ItemCreate):
    """アイテムを1件作成"""
    db_item = models.Item(title=item.title, content=item.content)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item_update: schemas.ItemUpdate):
    """IDで指定したアイテムを更新"""
    db_item = get_item(db, item_id)
    if db_item is None:
        return None
    
    # 更新するフィールドのみをセット
    update_data = item_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
        
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    """IDで指定したアイテムを削除"""
    db_item = get_item(db, item_id)
    if db_item is None:
        return None
    db.delete(db_item)
    db.commit()
    return db_item