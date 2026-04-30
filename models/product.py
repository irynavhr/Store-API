from sqlalchemy import Column, Integer, String, Float
from db import Base

from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    category = Column(String, index=True)

    order_items = relationship("OrderItem", back_populates="product")