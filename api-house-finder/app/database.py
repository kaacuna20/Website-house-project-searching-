from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ


DATABASE_URL = environ.get('DB_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # Update this to the new usage

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()