from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate, UserLogin
from services.auth_service import login_user, register_user
from core.dependencies import get_current_user
from db import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

# REGISTER 
@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user_data.email, user_data.password)

# LOGIN
@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, data.email, data.password)

# AUTHORIZE WITH TOKEN
@router.get("/me")
def get_me(user: User = Depends(get_current_user)):
    return user 