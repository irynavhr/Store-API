from pydantic import BaseModel, Field
from models.order import OrderStatus
from datetime import datetime
from schemas.user import UserPreview

# ORDER ITEM RESPONSE MODEL
class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price: float

    # ALLOWS ORM OBJECTS TO BE TRANSFORMED TO json
    class Config:
        from_attributes = True


# ORDER RESPONSE MODEL
class OrderResponse(BaseModel):
    id: int
    total_price: float
    created_at: datetime
    status: str
    user: UserPreview
    items: list[OrderItemResponse]
    
    # ALLOWS ORM OBJECTS TO BE TRANSFORMED TO json
    class Config:
        from_attributes = True

# ORDER STATUS UPDATE - admin
class OrderStatusUpdate(BaseModel):
    status: OrderStatus = Field(
        description="Available: pending, confirmed, shipped, cancelled"
    )