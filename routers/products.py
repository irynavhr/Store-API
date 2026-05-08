from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from schemas.product import ProductCreate, ProductResponse, ProductUpdate
from services import product_service
from core.dependencies import get_current_user, is_it_admin

router = APIRouter(prefix="/products", tags=["Products"])

# CREATE PRODUCT ENDPOINT
@router.post("/", response_model=ProductResponse)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(is_it_admin),
):
    return product_service.create_product(db, data)

# GET PRODUCTS LIST ENDPOINT
@router.get("/", response_model=list[ProductResponse])
def get_products(
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    category: str | None = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    return product_service.get_products(
        db, search, min_price, max_price, category, limit, offset
    )

# UPDATE PRODUCT BY ID  ENDPOINT
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    user=Depends(is_it_admin),
):
    product = product_service.update_product(db, product_id, data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# DELETE PRODUCT BY ID ENDPOINT
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(is_it_admin),
):
    result = product_service.delete_product(db, product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"ok": True}