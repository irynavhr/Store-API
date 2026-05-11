from sqlalchemy import Column, DateTime, Integer, String, func
from db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    subject = Column(String, nullable=False)
    message = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())  


    user = relationship("User", back_populates="messages")

