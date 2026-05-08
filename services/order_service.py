from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from models.order import Order
from models.orderItem import OrderItem
from models.cart import Cart
from models.cart_items import CartItem
from models.user import User

# CART TO ORDER
def create_order(db: Session, current_user: User):
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

    # CREATE ALL ORDER ITEMS AND CALC TOT PRICE
    for item in cart.items:

        item_total = item.product.price * item.quantity
        total_price += item_total

        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )

        db.add(order_item)
    # UPDATE TOT PRICE IN ORDER
    order.total_price = total_price
    # CLEAR CART
    for item in cart.items:
        db.delete(item)
    # COMMIT ALL CHANGES
    db.commit()
    db.refresh(order)

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
    return order