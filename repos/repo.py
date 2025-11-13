import aiosqlite
from typing import List, Optional
from datetime import datetime
from models.data_models import InventoryItem
from constants import DB_NAME, TABLE_NAME


class Repo:
    def __init__(self, db_path: str = DB_NAME):
        self.db_path = db_path

    async def init_db(self):
        """Initialize the inventory and supplier tables if they don't exist."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id TEXT PRIMARY KEY,
                    item_name TEXT NOT NULL,
                    category TEXT,
                    quantity INTEGER NOT NULL,
                    reorder_level INTEGER DEFAULT 0,
                    supplier TEXT,
                    unit_price REAL NOT NULL,
                    last_updated TEXT
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS Suppliers (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    contact_person TEXT,
                    phone_number TEXT,
                    category TEXT,
                    address TEXT
                )
            """)
            await db.commit()

    async def insert(self, item: InventoryItem):
        """Insert a new inventory record."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f"""
                INSERT INTO {TABLE_NAME} 
                (id, item_name, category, quantity, reorder_level, supplier, unit_price, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.id,
                item.item_name,
                item.category,
                item.quantity,
                item.reorder_level,
                item.supplier,
                item.unit_price,
                datetime.utcnow().isoformat()
            ))
            await db.commit()

    async def get(self, item_id: str) -> Optional[InventoryItem]:
        """Get a single inventory item by ID."""
        query = f"""
            SELECT id, item_name, category, quantity, reorder_level, supplier, unit_price, last_updated
            FROM {TABLE_NAME} WHERE id = ?
        """
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(query, (item_id,))
            row = await cursor.fetchone()
            if row:
                return InventoryItem(
                    id=row[0],
                    item_name=row[1],
                    category=row[2],
                    quantity=row[3],
                    reorder_level=row[4],
                    supplier=row[5],
                    unit_price=row[6],
                    last_updated=datetime.fromisoformat(
                        row[7]) if row[7] else None
                )
            return None

    async def list(self) -> List[InventoryItem]:
        """List all inventory items."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(f"""
                SELECT id, item_name, category, quantity, reorder_level, supplier, unit_price, last_updated
                FROM {TABLE_NAME}
                ORDER BY last_updated DESC
            """)
            rows = await cursor.fetchall()
            return [
                InventoryItem(
                    id=row[0],
                    item_name=row[1],
                    category=row[2],
                    quantity=row[3],
                    reorder_level=row[4],
                    supplier=row[5],
                    unit_price=row[6],
                    last_updated=datetime.fromisoformat(
                        row[7]) if row[7] else None
                )
                for row in rows
            ]

    async def delete(self, item_id: str) -> int:
        """Delete an inventory item by ID."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(f"DELETE FROM {TABLE_NAME} WHERE id = ?", (item_id,))
            await db.commit()
            return cursor.rowcount

    async def update(self, item: InventoryItem) -> bool:
        """Update an existing inventory item."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(f"""
                UPDATE {TABLE_NAME}
                SET item_name = ?, category = ?, quantity = ?, reorder_level = ?, 
                    supplier = ?, unit_price = ?, last_updated = ?
                WHERE id = ?
            """, (
                item.item_name,
                item.category,
                item.quantity,
                item.reorder_level,
                item.supplier,
                item.unit_price,
                datetime.utcnow().isoformat(),
                item.id
            ))
            await db.commit()
            return cursor.rowcount > 0

    async def insert_supplier(self, supplier):
        """Insert a new supplier record."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO Suppliers (id, name, contact_person, phone_number, category, address)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (supplier.id, supplier.name, supplier.contact_person, supplier.phone_number, supplier.category, supplier.address))
            await db.commit()

    async def list_suppliers(self):
        """List all suppliers."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT id, name, contact_person, phone_number, category, address FROM Suppliers")
            rows = await cursor.fetchall()
            return [{
                "id": row[0], "name": row[1], "contact_person": row[2],
                "phone_number": row[3], "category": row[4], "address": row[5]
            } for row in rows]
