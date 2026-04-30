from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from core.jwt import decode_token
from db import get_db
from models.user import User


# функція авторизіції в сваггері
from fastapi.security import HTTPBearer
oauth2_scheme = HTTPBearer()

# дістаємо дані користувача з токена
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    
    token = credentials.credentials
    
    user_data = decode_token(token)

    if user_data is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = user_data.get("sub")  # дістаємо id користувача з токена

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user



def is_it_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user
