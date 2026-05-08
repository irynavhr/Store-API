from sqlalchemy import Column, Integer, String, Float
from db import Base

from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    description = Column(String)
    category = Column(String, index=True)
    price = Column(Float, nullable=False)
    discount_persent = Column(Float, default=0.0)

    order_items = relationship("OrderItem", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")