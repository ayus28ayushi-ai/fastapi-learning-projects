from enum import Enum
from datetime import  datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field

# order status
class OrderStatus(str, Enum):
    PREPARING = "preparing"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"

# database table
class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    delivery_address: str
    items: str
    status: OrderStatus = Field(default=OrderStatus.PREPARING)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class OrderCreated(SQLModel):
    customer_name: str
    delivery_address:str
    items:str

class OrderUpdate(SQLModel):
    status: OrderStatus = Field(default = OrderStatus.PREPARING)
    delivery_address: Optional[str] = Field(default=None)

class StatusLog(SQLModel):
    order_id: int
    order_status: OrderStatus
    new_status: OrderStatus
    changed_at: datetime