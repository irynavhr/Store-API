from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from core.dependencies import get_current_user

from services import cart_service
from schemas.cart import (
    AddToCartRequest,
    UpdateCartItemRequest,
    CartResponse
)


router = APIRouter(prefix="/cart", tags=["Cart"])


# ADD ITEM TO CART
@router.post("/items")
def add_to_cart(
    data: AddToCartRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return cart_service.add_to_cart(db, user.id, data.product_id, data.quantity)


# REMOVE ITEM FROM CART
@router.delete("/items/{product_id}")
def remove_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return cart_service.remove_from_cart(db, user.id, product_id)


# UPDATE ITEM QUANTITY
@router.patch("/items")
def update_cart_item(
    data: UpdateCartItemRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return cart_service.update_quantity(
        db,
        user.id,
        data.product_id,
        data.quantity
    )


# GET CART
@router.get("/", response_model=CartResponse)
def get_cart(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return cart_service.get_cart(db, user.id)


# CLEAR CART 
@router.delete("/clear")
def clear_cart(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return cart_service.clear_cart(db, user.id)