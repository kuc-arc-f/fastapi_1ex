from pydantic import BaseModel
from datetime import datetime

# ベースとなるスキーマ
class ItemBase(BaseModel):
    title: str | None = None
    content: str | None = None

# アイテム作成時に受け取るデータ
class ItemCreate(ItemBase):
    title: str
    content: str

# アイテム更新時に受け取るデータ
class ItemUpdate(ItemBase):
    pass

# APIから返すデータ（DBから読み取ったデータ）
class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    # SQLAlchemyモデルからPydanticモデルへ変換するための設定
    class Config:
        from_attributes = True # Pydantic V2
        # orm_mode = True # Pydantic V1