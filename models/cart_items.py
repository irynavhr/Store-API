from db import Base
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from datetime import datetime, timezone

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class CartItem(Base):
    __tablename__ = "cart_items"

    __table_args__ = (
        UniqueConstraint("cart_id", "product_id"),)

    id = Column(Integer, primary_key=True)

    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", back_populates="cart_items")
    
