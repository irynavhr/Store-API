from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from services.order_service import (
    create_order,
    get_my_orders
)
from core.dependencies import get_current_user
from models.user import User
from schemas.order import OrderResponse


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post(
    "/",
    response_model=OrderResponse
)
def create_new_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return create_order(db, current_user)


@router.get(
    "/my",
    response_model=list[OrderResponse]
)
def get_user_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_my_orders(db, current_user)