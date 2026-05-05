from sqlalchemy import Column, Integer, String
from db import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")

    orders = relationship("Order", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")
    carts = relationship("Cart", back_populates="user")
    messages = relationship("Message", back_populates="user")
