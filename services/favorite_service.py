from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from models.favorite import Favorite
from models.user import User
from models.product import Product


# ADD PRODUCT TO FAVORITES
def add_to_favorites(db: Session, current_user: User, data):

    product = db.query(Product).filter(
        Product.id == data.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    existing_favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.product_id == data.product_id
    ).first()

    if existing_favorite:
        raise HTTPException(
            status_code=400,
            detail="Product already in favorites"
        )

    favorite = Favorite(
        user_id=current_user.id,
        product_id=data.product_id
    )

    db.add(favorite)

    db.commit()
    db.refresh(favorite)

    return favorite


# REMOVE PRODUCT FROM FAVORITES
def remove_from_favorites(db: Session, current_user: User, product_id: int):
    

    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.product_id == product_id
    ).first()

    if not favorite:
        raise HTTPException(
            status_code=404,
            detail="Favorite not found"
        )

    db.delete(favorite)

    db.commit()

    return {"message": "Removed from favorites"}


# GET FAVORITES FOR CURRENT USER
def get_favorites(db: Session, current_user: User):
    favorites = (
        db.query(Favorite)
        .options(joinedload(Favorite.product))
        .filter(Favorite.user_id == current_user.id)
        .all()
    )
    return favorites