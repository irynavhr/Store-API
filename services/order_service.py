from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from models.order import Order
from models.orderItem import OrderItem
from models.cart import Cart
from models.cart_items import CartItem
from models.user import User
from services.email_service import send_order_created_email, send_order_status_email

# CART TO ORDER
def create_order(db: Session, current_user: User, bonus_to_spend: int):
    # LOAD CART WITH ITEMS AND PRODUCTS
    cart = (
        db.query(Cart)
        .options(
            joinedload(Cart.items).joinedload(CartItem.product)
        )
        .filter(Cart.user_id == current_user.id)
        .first()
    )
    # IF NO CART
    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )
    #  IF CART IS EMPTY
    if not cart.items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    
    total_price = 0
    # CREATE ORDER
    order = Order(
        user_id=current_user.id,
        status="pending",
        total_price=0
    )
    # ADD ORDER TO DB TO GET ID
    db.add(order)
    db.flush()

    # CREATE ORDER ITEMS and CALC TOT PRICE with DISCOUNTS
    for item in cart.items:
        discounted_price = item.product.price * (1 - item.product.discount_persent)
        item_total = discounted_price * item.quantity
        total_price += item_total

        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=discounted_price
        )

        db.add(order_item)

    # APPLY BONUSES
    max_bonus_allowed = int(total_price * 0.2)
    if bonus_to_spend > max_bonus_allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Too many bonuses. Max allowed is {max_bonus_allowed}"
        )
    
    total_price -= bonus_to_spend # APPLY BONUSES 
    current_user.bonus_balance -= bonus_to_spend # SPEND BONUSES

    # IF FIRST ODER - EARNX2 BONUSES
    previous_orders = db.query(Order).filter(
        Order.user_id == current_user.id
    ).count()
    bonus_rate = 0.2 if previous_orders == 1 else 0.1
    bonuses_earned = int(total_price * bonus_rate)
    current_user.bonus_balance += bonuses_earned  # EARN NEW BONUSES

    # UPDATE TOT PRICE IN ORDER
    order.total_price = total_price

    # CLEAR CART
    for item in cart.items:
        db.delete(item)
    # COMMIT ALL CHANGES
    db.commit()
    db.refresh(order)

    send_order_created_email(current_user.email, order.id, bonuses_earned, current_user.bonus_balance)

    return order

# GET ORDERS FOR CURRENT USER
def get_my_orders(db: Session, current_user: User):

    orders = (
        db.query(Order)
        .options(
            joinedload(Order.items)
        )
        .filter(Order.user_id == current_user.id)
        .all()
    )

    return orders

# GET ALL ORDERS (ADMIN ONLY)
def get_all_orders_of_all_users(db: Session):
    return db.query(Order).options(joinedload(Order.items)).all()
    # options(joinedload(Order.items))


# UPDATE ORDER STATUS (ADMIN ONLY)
def update_status_of_order(db: Session, order_id: int, new_status: str):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.status = new_status
    db.commit()
    db.refresh(order)

    send_order_status_email(order.user.email, order.id, order.status)

    return order