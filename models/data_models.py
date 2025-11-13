from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class InventoryItem(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: lambda dt: dt.isoformat()})
    id: str
    item_name: str
    # e.g., Spare Parts, Tools, Accessories
    category: Optional[str] = None
    quantity: int
    reorder_level: Optional[int] = 0        # Minimum stock before reorder
    supplier: Optional[str] = None
    unit_price: float                       # Cost per unit/item
    last_updated: Optional[datetime] = None  # Auto-update on edit
