from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from services import favorite_service
from core.dependencies import get_current_user
from models.user import User    
from schemas.favorite import FavoriteCreate, FavoriteResponse

router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"]
)

# ADD PRODUCT TO FAVORITES
@router.post("/", response_model=FavoriteResponse)
def add_to_favorites(
    data: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return favorite_service.add_to_favorites(db, current_user, data)

# REMOVE PRODUCT FROM FAVORITES
@router.delete("/remove/{product_id}")
def remove_from_favorites(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return favorite_service.remove_from_favorites(
        db,
        current_user,
        product_id
    )


# GET FAVORITES FOR CURRENT USER
@router.get("/", response_model=list[FavoriteResponse])
def get_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return favorite_service.get_favorites(db, current_user)