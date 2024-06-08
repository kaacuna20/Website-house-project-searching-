from fastapi import Depends, HTTPException, status, Header
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
import datetime
from typing import List, Optional
from os import environ
from app.database import get_db
from app.models import User
import logging

SECRET_KEY = environ.get('SECRET_APP_KEY')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ApiKeyException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Sorry, that's not allowed. Make sure you have the correct api_key or apikey expired.")


class TokenException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate token, you are not autorizated or token expire!")


async def get_user_by_api_key(db: Session, api_key: str) -> Optional[User]:
    logger.info(f"Checking API key: {api_key}")
    return db.query(User).filter(User.api_key == api_key).first()


async def get_user_by_token(db: Session, token: str) -> Optional[User]:
        return db.query(User).filter(User.token_secret == token).first()
       

async def api_key_auth(api_key: str = Depends(APIKeyHeader(name="Api-Key")), db: Session = Depends(get_db)):
    logger.info(f"Received API key: {api_key}")
    user = await get_user_by_api_key(db, api_key)
    if user is None or user.api_key_expires < datetime.datetime.now():
        logger.warning(f"API key authentication failed for key: {api_key}")
        raise ApiKeyException()
    logger.info(f"Authenticated user: {user.username}")
    return user


async def token_auth(token_secret: str = Header(None), db: Session = Depends(get_db)):
    
    if token_secret is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is required")

    user = await get_user_by_token(db, token_secret)
   
    if user is None or user.token_secret_expires < datetime.datetime.now():
        raise TokenException()

    return user