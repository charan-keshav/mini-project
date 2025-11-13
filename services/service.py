from typing import List
from fastapi import HTTPException
from models.data_models import InventoryItem
from repos.repo import Repo


class Service:
    def __init__(self, repo: Repo):
        self.repo = repo

    async def create_inventory_item(self, item: InventoryItem):
        """Create a new inventory item record"""
        await self.repo.init_db()
        if isinstance(item, dict):
            item = InventoryItem(**item)
        existing = await self.repo.get(item.id)
        if existing:
            raise HTTPException(
                status_code=409, detail="Inventory item already exists")
        await self.repo.insert(item)
        return item

    async def update_inventory_item(self, item_id: str, item: InventoryItem) -> InventoryItem:
        """Update an existing inventory item"""
        await self.repo.init_db()
        if isinstance(item, dict):
            item = InventoryItem(**item)
        item.id = item_id
        updated = await self.repo.update(item)
        if not updated:
            raise HTTPException(
                status_code=404, detail="Inventory item not found to update")
        return item

    async def delete_inventory_item(self, item_id: str):
        """Delete an inventory item"""
        await self.repo.init_db()
        deleted_count = await self.repo.delete(item_id)
        if deleted_count == 0:
            raise HTTPException(
                status_code=404, detail="Inventory item not found to delete")
        return {"message": f"Inventory item with id {item_id} deleted successfully"}

    async def get_all_inventory_items(self) -> List[InventoryItem]:
        """Retrieve all inventory items"""
        await self.repo.init_db()
        return await self.repo.list()
