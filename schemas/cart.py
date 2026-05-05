from pydantic import BaseModel
from pydantic import BaseModel, Field


class AddToCartRequest(BaseModel):
    product_id: int


class UpdateCartItemRequest(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)  # > 0


class CartItemResponse(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int
    subtotal: float


class CartResponse(BaseModel):
    items: list[CartItemResponse]
    total: float