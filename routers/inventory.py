from fastapi import APIRouter, status
from typing import List
from models.data_models import InventoryItem
from services.service import Service
from repos.repo import Repo
from constants import DB_NAME

router = APIRouter()
repo = Repo(DB_NAME)
service = Service(repo)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_inventory_item(item: InventoryItem):
    """Create a new inventory item"""
    return await service.create_inventory_item(item)


@router.put("/{item_id}", status_code=status.HTTP_200_OK)
async def update_inventory_item(item_id: str, item: InventoryItem):
    """Update an existing inventory item"""
    return await service.update_inventory_item(item_id, item)


@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def delete_inventory_item(item_id: str):
    """Delete an inventory item"""
    return await service.delete_inventory_item(item_id)


@router.get("/", response_model=List[InventoryItem])
async def get_all_inventory_items():
    """Retrieve all inventory items"""
    return await service.get_all_inventory_items()
