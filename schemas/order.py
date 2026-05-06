from pydantic import BaseModel

class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price: float

    # ALLOWS ORM OBJECTS TO BE TRANSFORMED TO RESPONSE
    class Config:
        orm_mode = True 



class OrderResponse(BaseModel):
    id: int
    total_price: float
    status: str
    items: list[OrderItemResponse]
    
    # ALLOWS ORM OBJECTS TO BE TRANSFORMED TO RESPONSE
    class Config:
        orm_mode = True