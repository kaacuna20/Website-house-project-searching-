from fastapi import Depends, HTTPException, status, Header
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
import datetime
from typing import Optional
from os import environ
from cryptography.fernet import Fernet, InvalidToken
from app.database import get_db
from app.models.db_models import User
from app.logs.log import Logger

logger = Logger()

SECRET_KEY = environ.get('SECRET_APP_KEY')
ENCRYPTION_KEY = environ.get('ENCRYPTION_KEY')

cipher_suite = Fernet(ENCRYPTION_KEY)


class PublicApiKeyException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Sorry, that's not allowed. Make sure you have the correct public_api_key or public_api_key expired!")

class SecretApiKeyException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Sorry, that's not allowed. Make sure you have the correct secret_api_key or secret_api_key expired!")

async def get_user_by_public_api_key(db: Session, public_api_key: str) -> Optional[User]:
    user = db.query(User).filter_by(public_api_key=public_api_key, is_active=True).first()
    if user:
        return user
    return None

async def authenticate_secret_api_key(user: User, secret_api_key: str) -> bool:
    try:
        decrypted_key = cipher_suite.decrypt(user.secret_api_key.encode('utf-8')).decode('utf-8')
        return decrypted_key == secret_api_key
    except InvalidToken:
        return False

async def public_api_key_auth(public_api_key: str = Header(None, alias="x-api-public-key"), db: Session = Depends(get_db)):
    user = await get_user_by_public_api_key(db, public_api_key)
    if user is None or user.public_api_key_expires < datetime.datetime.now():
        logger.warning(f"PUBLIC_API_KEY authentication failed for key: {public_api_key}")
        raise PublicApiKeyException()
    logger.info(f"Authenticated user: {user.username}")
    return user

async def secret_api_key_auth(secret_api_key: str = Header(None, alias="x-api-secret-key"), user: User = Depends(public_api_key_auth)):
    if secret_api_key is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="secret_api_key is required")

    if not await authenticate_secret_api_key(user, secret_api_key) or user.secret_api_key_expires < datetime.datetime.now():
        logger.warning(f"SECRET_API_KEY authentication failed for user: {user.username}")
        raise SecretApiKeyException()

    return user

async def combined_auth(
    public_user: User = Depends(public_api_key_auth),
    secret_user: User = Depends(secret_api_key_auth)
) -> User:
    if public_user.user_id != secret_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Mismatched public and secret API keys")
    return public_user
