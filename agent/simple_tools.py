from services.service import Service
from repos.repo import Repo
from constants import DB_NAME

repo = Repo(DB_NAME)
service = Service(repo)

async def get_inventory():
    """Get all inventory items"""
    items = await service.get_all_inventory_items()
    return [{"name": item.item_name, "quantity": item.quantity, "category": item.category} for item in items]

async def count_items():
    """Count total inventory items"""
    items = await service.get_all_inventory_items()
    return {"count": len(items)}

async def check_stock(item_name: str):
    """Check if item is in stock"""
    items = await service.get_all_inventory_items()
    item = next((i for i in items if item_name.lower() in i.item_name.lower()), None)
    return {"found": bool(item), "quantity": item.quantity if item else 0}