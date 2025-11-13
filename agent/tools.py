from services.service import Service
from repos.repo import Repo
from constants import DB_NAME

repo = Repo(DB_NAME)
service = Service(repo)

# Fetch all inventory items
async def get_inventory() -> dict:
    return await service.get_all_inventory_items()