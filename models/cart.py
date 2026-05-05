from db import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # зв'язки
    items = relationship("CartItem", back_populates="cart", cascade="all, delete")
    user = relationship("User", back_populates="carts")
    