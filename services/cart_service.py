from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

import db
from models.cart import Cart
from models.cart_items import CartItem
from models.product import Product


#  GET OR CREATE CART
def get_or_create_cart(db: Session, user_id: int):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    # IF EXISTS
    if cart:
        return cart
    # IF NOT - CREATE NEW
    cart = Cart(user_id=user_id)
    db.add(cart)
    # COMMIT AND REFRESH
    try:
        db.commit()
        db.refresh(cart)
    except IntegrityError:
        db.rollback()
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    return cart


#  ADD TO CART
def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart = get_or_create_cart(db, user_id)

    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    ).first()

    if item:
        item.quantity += quantity
    else:
        item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(item)

    db.commit()
    db.refresh(item)

    return item




# DELETE FROM CART
def remove_from_cart(db: Session, user_id: int, product_id: int):
    cart = get_or_create_cart(db, user_id)

    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not in cart")

    db.delete(item)
    db.commit()

    return {"message": "Item removed from cart"}


# CALCULATE CART TOTAL
def calculate_cart_total(cart: Cart):
    total = 0

    for item in cart.items:
        total += item.quantity * item.product.price

    return total


# GET CART 
def get_cart(db: Session, user_id: int):
    cart = get_or_create_cart(db, user_id)

    items = []

    for item in cart.items:
        items.append({
            "product_id": item.product.id,
            "name": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity,
            "subtotal": item.quantity * item.product.price
        })

    total = calculate_cart_total(cart)

    return {
        "items": items,
        "total": total
    }


# CLEAR CART
def clear_cart(db: Session, user_id: int):
    cart = get_or_create_cart(db, user_id)

    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()

    return {"message": "Cart cleared"}

# UPDATE CART ITEM QUANTITY
def update_quantity(db: Session, user_id: int, product_id: int, quantity: int):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Invalid quantity")

    cart = get_or_create_cart(db, user_id)

    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.quantity = quantity
    db.commit()

    return item