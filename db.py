from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# VAR FROM .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLALCHEMY SETUP - (CREATE DB CONN & POOL)
engine = create_engine(DATABASE_URL)

# SESSION CONFIG FOR DB INTERACTIONS
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# BASE CLASS FOR ALL ORM MODELS   
Base = declarative_base()


# DEPENDENCY TO GET DB SESSION FOR EACH REQUEST
def get_db():
    db = SessionLocal()
    try:
        yield db      # YIELD SESSION
    finally:
        db.close()    # CLOSE SESION (RETURN CONN TO THE POOL)