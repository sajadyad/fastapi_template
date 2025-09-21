from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_items_service
from app.schema.response import StandardResponse

from ..schema.item import ItemCreate, ItemOut, ItemUpdate
from ..service.item import ItemsService

router = APIRouter()


@router.post(
    "/", response_model=StandardResponse[ItemOut], status_code=status.HTTP_201_CREATED
)
async def create_item(
    payload: ItemCreate, service: ItemsService = Depends(get_items_service)
):
    return await service.create_item(payload)


@router.get("/", response_model=StandardResponse[List[ItemOut]])
async def list_items(
    limit: int = 100, service: ItemsService = Depends(get_items_service)
):
    return await service.list_items(limit)


@router.get("/{item_id}", response_model=StandardResponse[ItemOut])
async def read_item(item_id: int, service: ItemsService = Depends(get_items_service)):
    obj = await service.get_item(item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    return obj


@router.put("/{item_id}", response_model=StandardResponse[ItemOut])
async def update_item(
    item_id: int,
    payload: ItemUpdate,
    service: ItemsService = Depends(get_items_service),
):
    obj = await service.update_item(item_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    return obj
