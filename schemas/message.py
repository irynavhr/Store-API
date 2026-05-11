from datetime import datetime
from pydantic import BaseModel, Field

# CREATE
class MessageCreate(BaseModel):

    subject: str = Field(
        min_length=3,
        max_length=100
    )

    message: str = Field(
        min_length=5,
        max_length=1000
    )

# RESPONSE
class MessageResponse(BaseModel):

    id: int

    subject: str

    message: str

    created_at: datetime

    user_id: int

    class Config:
        orm_mode = True