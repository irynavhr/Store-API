from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserPreview(BaseModel):
    id: int
    email: str
    bonus_balance: int

    class Config:
        from_attributes = True