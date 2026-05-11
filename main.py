from fastapi import FastAPI
from db import Base, engine
from models import user, product, order, orderItem, cart, cart_items, favorite, message

from routers.auth import router as auth_router
from routers.products import router as products_router
from routers.carts import router as carts_router
from routers.orders import router as order_router
from routers.favorites import router as favorites_router
from routers.messages import router as messages_router



# INITIALIZE THE FASTAPI APP
app = FastAPI()

# CREATE TABLES IF THEY ARE NOT IN THE DATABASE
Base.metadata.create_all(bind=engine)

# ROOT/TEST ENDPOINT
@app.get("/")
def root():
    return {"message": "API is running!"}

# INCLUDE THE SUB ROUTERS
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(carts_router)
app.include_router(order_router)
app.include_router(favorites_router)
app.include_router(messages_router)