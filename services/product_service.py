from sqlalchemy.orm import Session
from models.product import Product


# CREATE PRODUCT
def create_product(db: Session, data):
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

# GET PRODUCTS WITH FILTERS
def get_products(
    db: Session,
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    category: str | None = None,
    limit: int = 10,
    offset: int = 0,
):
    query = db.query(Product)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    if min_price:
        query = query.filter(Product.price >= min_price)

    if max_price:
        query = query.filter(Product.price <= max_price)

    if category:
        query = query.filter(Product.category == category)

    return query.offset(offset).limit(limit).all()

# UPDATE PRODUCT BY ID
def update_product(db: Session, product_id: int, data):
    product = db.query(Product).get(product_id)
    if not product:
        return None

    for key, value in data.dict().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

# DELETE PRODUCT BY ID
def delete_product(db: Session, product_id: int):
    product = db.query(Product).get(product_id)
    if not product:
        return None

    db.delete(product)
    db.commit()
    return True