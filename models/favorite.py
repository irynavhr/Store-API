from db import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    user = relationship("User", back_populates="favorites")
    product = relationship("Product")

    