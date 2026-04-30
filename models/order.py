from db import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())  
    status = Column(String, default="pending")

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")