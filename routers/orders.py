from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from services.order_service import (
    create_order,
    get_my_orders,
    get_all_orders_of_all_users,
    update_status_of_order
)
from core.dependencies import get_current_user, is_it_admin
from models.user import User
from schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# CREATE ORDER FROM CART 
@router.post(
    "/",
    response_model=OrderResponse
)
def create_new_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return create_order(db, current_user, order_data.bonus_to_spend)

# GET ORDERS FOR CURRENT USER
@router.get(
    "/my",
    response_model=list[OrderResponse]
)
def get_user_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_my_orders(db, current_user)

# GET ALL ORDERS (ADMIN ONLY)
@router.get("/",
    response_model=list[OrderResponse])
def get_all_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(is_it_admin)
):
    return get_all_orders_of_all_users(db)

# UPDATE ORDER STATUS (ADMIN ONLY)
@router.patch("/{order_id}/status")
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(is_it_admin)
):
    return update_status_of_order(db, order_id, status_data.status)