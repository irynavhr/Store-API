from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    category: str | None = None
    price: float
    discount_persent: float | None = 0.0


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True