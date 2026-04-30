from db import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)

    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Integer)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    
