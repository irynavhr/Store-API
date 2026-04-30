from sqlalchemy import Column, Integer, String
from db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)


    user = relationship("User", back_populates="messages")

