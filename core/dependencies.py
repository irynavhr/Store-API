from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer

from core.jwt import decode_token
from db import get_db
from models.user import User



# FETCH TOKEN FROM HEADER
oauth2_scheme = HTTPBearer()

# CHECK USER AND RETURN IT, IF TOKEN IS VALID, IF NOT - THROW 401
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

# IF USER IS NOT ADMIN - THROW 403, ELSE RETURN USER
def is_it_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user
