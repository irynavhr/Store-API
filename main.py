from fastapi import FastAPI
from db import Base, engine
from models import user, product, order, orderItem, cart_items, favorite, message
from routers import products
from routers.auth import router as auth_router
from routers.products import router as products_router




app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "API is running!"}

app.include_router(auth_router)
app.include_router(products_router)


