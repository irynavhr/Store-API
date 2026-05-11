from pydantic import BaseModel
from schemas.product import ProductResponse



# CREATE
class FavoriteCreate(BaseModel):
    product_id: int

# RESPONSE
class FavoriteResponse(BaseModel):
    id: int
    product: ProductResponse

    class Config:
        from_attributes = True