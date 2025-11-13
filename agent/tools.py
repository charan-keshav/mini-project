from services.service import Service
from repos.repo import Repo
from constants import DB_NAME
from models.data_models import InventoryItem, Supplier
from datetime import datetime, timedelta
import random
from typing import List, Optional

repo = Repo(DB_NAME)
service = Service(repo)

# Fetch all inventory items
async def get_inventory() -> List[dict]:
    items = await service.get_all_inventory_items()
    return [{"id": item.id, "item_name": item.item_name, "category": item.category, "quantity": item.quantity, "reorder_level": item.reorder_level, "supplier": item.supplier, "unit_price": item.unit_price} for item in items]

# Get items by category
async def get_items_by_category(category: str) -> List[dict]:
    """Get all items belonging to a specific category"""
    items = await service.get_all_inventory_items()
    filtered_items = [item for item in items if item.category and category.lower() in item.category.lower()]
    return [{"item_name": item.item_name, "quantity": item.quantity, "category": item.category} for item in filtered_items]

# Get items needing reordering
async def get_items_needing_reorder() -> List[dict]:
    """Get all items where quantity is below reorder level"""
    items = await service.get_all_inventory_items()
    reorder_items = [item for item in items if item.quantity < item.reorder_level]
    return [{"item_name": item.item_name, "current_quantity": item.quantity, "reorder_level": item.reorder_level, "shortage": item.reorder_level - item.quantity} for item in reorder_items]

# Check stock status of specific item
async def check_item_stock(item_name: str) -> dict:
    """Check if a specific item is in stock"""
    items = await service.get_all_inventory_items()
    item = next((item for item in items if item_name.lower() in item.item_name.lower()), None)
    
    if not item:
        return {"found": False, "message": f"{item_name} not found in inventory"}
    
    return {"found": True, "item_name": item.item_name, "quantity": item.quantity, "in_stock": item.quantity > 0, "status": "IN STOCK" if item.quantity > 0 else "OUT OF STOCK"}

# Update item quantity
async def update_item_quantity(item_name: str, new_quantity: int) -> dict:
    """Update the quantity of a specific item"""
    items = await service.get_all_inventory_items()
    item = next((item for item in items if item_name.lower() in item.item_name.lower()), None)
    
    if not item:
        new_item = InventoryItem(id=str(random.randint(1000000000000, 9999999999999)), item_name=item_name, category="Spare Parts", quantity=new_quantity, reorder_level=5, supplier="Default Supplier", unit_price=0.0, last_updated=datetime.utcnow())
        await service.create_inventory_item(new_item)
        return {"success": True, "message": f"Created new item '{item_name}' with quantity {new_quantity}"}
    
    item.quantity = new_quantity
    await service.update_inventory_item(item.id, item)
    return {"success": True, "message": f"Updated '{item_name}' quantity to {new_quantity}"}

# Remove item from inventory
async def remove_item(item_name: str) -> dict:
    """Remove a specific item from inventory"""
    items = await service.get_all_inventory_items()
    item = next((item for item in items if item_name.lower() in item.item_name.lower()), None)
    
    if not item:
        return {"success": False, "message": f"{item_name} not found in inventory"}
    
    await service.delete_inventory_item(item.id)
    return {"success": True, "message": f"Removed '{item_name}' from inventory"}

# Add sample data
async def add_sample_inventory_data() -> dict:
    """Add sample repair inventory data to the database"""
    sample_items = [
        {"item_name": "Air Filter", "category": "Spare Parts", "quantity": 15, "reorder_level": 5, "supplier": "Auto Parts Co", "unit_price": 12.50},
        {"item_name": "Brake Pads", "category": "Spare Parts", "quantity": 8, "reorder_level": 3, "supplier": "Brake Systems Ltd", "unit_price": 45.00},
        {"item_name": "Screwdriver Set", "category": "Tools", "quantity": 4, "reorder_level": 2, "supplier": "Tool Supply Co", "unit_price": 25.00},
        {"item_name": "Engine Oil", "category": "Spare Parts", "quantity": 20, "reorder_level": 10, "supplier": "Oil Distributors", "unit_price": 8.75}
    ]
    
    added_count = 0
    for item_data in sample_items:
        existing_items = await service.get_all_inventory_items()
        if not any(existing.item_name.lower() == item_data["item_name"].lower() for existing in existing_items):
            item = InventoryItem(id=str(random.randint(1000000000000, 9999999999999)), item_name=item_data["item_name"], category=item_data["category"], quantity=item_data["quantity"], reorder_level=item_data["reorder_level"], supplier=item_data["supplier"], unit_price=item_data["unit_price"], last_updated=datetime.utcnow())
            await service.create_inventory_item(item)
            added_count += 1
    
    return {"success": True, "message": f"Added {added_count} sample inventory items to the database"}

# Analytics functions
async def get_inventory_count() -> dict:
    """Get total count of inventory items"""
    items = await service.get_all_inventory_items()
    return {"total_items": len(items)}

async def get_total_stock_value() -> dict:
    """Calculate total stock value (quantity * unit_price)"""
    items = await service.get_all_inventory_items()
    total_value = sum(item.quantity * item.unit_price for item in items)
    return {"total_value": round(total_value, 2)}

async def get_top_supplier() -> dict:
    """Find supplier that provides the most items"""
    items = await service.get_all_inventory_items()
    supplier_counts = {}
    for item in items:
        if item.supplier:
            supplier_counts[item.supplier] = supplier_counts.get(item.supplier, 0) + 1
    
    if not supplier_counts:
        return {"supplier": None, "count": 0}
    
    top_supplier = max(supplier_counts, key=supplier_counts.get)
    return {"supplier": top_supplier, "count": supplier_counts[top_supplier]}

# Auditing functions
async def get_last_updated_item() -> dict:
    """Get the inventory item that was last updated"""
    items = await service.get_all_inventory_items()
    if not items:
        return {"item_name": None, "last_updated": None}
    
    latest_item = max(items, key=lambda x: x.last_updated if x.last_updated else datetime.min)
    return {"item_name": latest_item.item_name, "last_updated": latest_item.last_updated.isoformat() if latest_item.last_updated else None}

async def get_items_not_updated_6_months() -> List[dict]:
    """Get items not updated in the last 6 months"""
    items = await service.get_all_inventory_items()
    six_months_ago = datetime.utcnow() - timedelta(days=180)
    
    old_items = []
    for item in items:
        if not item.last_updated or item.last_updated < six_months_ago:
            old_items.append({
                "item_name": item.item_name,
                "last_updated": item.last_updated.isoformat() if item.last_updated else "Never"
            })
    
    return old_items

async def get_category_highest_avg_price() -> dict:
    """Get category with highest average price"""
    items = await service.get_all_inventory_items()
    if not items:
        return {"category": None, "avg_price": 0}
    
    category_prices = {}
    for item in items:
        if item.category:
            if item.category not in category_prices:
                category_prices[item.category] = []
            category_prices[item.category].append(item.unit_price)
    
    if not category_prices:
        return {"category": None, "avg_price": 0}
    
    category_averages = {cat: sum(prices)/len(prices) for cat, prices in category_prices.items()}
    top_category = max(category_averages, key=category_averages.get)
    
    return {"category": top_category, "avg_price": round(category_averages[top_category], 2)}

# Multi-modal Supplier functions
async def create_supplier_model(name: str, contact_person: Optional[str] = None, phone_number: Optional[str] = None, category: Optional[str] = None, address: Optional[str] = None) -> dict:
    """Create a new supplier in the system"""
    from models.data_models import Supplier
    supplier = Supplier(
        id=str(random.randint(1000000000000, 9999999999999)),
        name=name,
        contact_person=contact_person,
        phone_number=phone_number,
        category=category,
        address=address
    )
    await service.create_supplier(supplier)
    return {"success": True, "message": f"Created supplier '{name}' successfully"}

async def get_supplier_lowest_reorder_frequency() -> dict:
    """Find supplier whose items have lowest reorder frequency"""
    items = await service.get_all_inventory_items()
    supplier_reorder_ratios = {}
    
    for item in items:
        if item.supplier and item.quantity > 0:
            reorder_ratio = item.quantity / item.reorder_level if item.reorder_level > 0 else float('inf')
            if item.supplier not in supplier_reorder_ratios:
                supplier_reorder_ratios[item.supplier] = []
            supplier_reorder_ratios[item.supplier].append(reorder_ratio)
    
    if not supplier_reorder_ratios:
        return {"supplier": None, "avg_ratio": 0}
    
    supplier_avg_ratios = {sup: sum(ratios)/len(ratios) for sup, ratios in supplier_reorder_ratios.items()}
    lowest_supplier = min(supplier_avg_ratios, key=supplier_avg_ratios.get)
    
    return {"supplier": lowest_supplier, "avg_ratio": round(supplier_avg_ratios[lowest_supplier], 2)}

async def get_supplier_highest_category_cost() -> dict:
    """Find supplier whose category items cost the most on average"""
    items = await service.get_all_inventory_items()
    supplier_category_costs = {}
    
    for item in items:
        if item.supplier and item.category:
            key = f"{item.supplier}_{item.category}"
            if key not in supplier_category_costs:
                supplier_category_costs[key] = []
            supplier_category_costs[key].append(item.unit_price)
    
    if not supplier_category_costs:
        return {"supplier": None, "category": None, "avg_cost": 0}
    
    supplier_category_avg = {key: sum(costs)/len(costs) for key, costs in supplier_category_costs.items()}
    highest_key = max(supplier_category_avg, key=supplier_category_avg.get)
    supplier, category = highest_key.split('_', 1)
    
    return {"supplier": supplier, "category": category, "avg_cost": round(supplier_category_avg[highest_key], 2)}