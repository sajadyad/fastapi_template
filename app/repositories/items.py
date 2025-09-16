from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.item import Item as ItemModel
from app.schemas.item import ItemCreate, ItemUpdate


class ItemsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, item_id: int) -> Optional[ItemModel]:
        q = await self.db.execute(select(ItemModel).where(ItemModel.id == item_id))
        return q.scalars().first()

    async def list(self, limit: int = 100) -> List[ItemModel]:
        q = await self.db.execute(select(ItemModel).limit(limit))
        return q.scalars().all()

    async def create(self, payload: ItemCreate) -> ItemModel:
        pass

    async def update(self, db_obj: ItemModel, payload: ItemUpdate) -> ItemModel:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj: ItemModel) -> None:
        await self.db.delete(db_obj)
        await self.db.commit()
