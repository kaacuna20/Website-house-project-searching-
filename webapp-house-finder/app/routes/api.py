from flask import Blueprint, jsonify
from flask_login import login_required, current_user
import jwt
import datetime
import pytz
from app.models import User
from app.models import db
from os import environ
import secrets
from cryptography.fernet import Fernet
from app.logs_system.log import Logger

logger = Logger()

api_bp = Blueprint('api', __name__)


ENCRYPTION_KEY = environ.get('ENCRYPTION_KEY')

cipher_suite = Fernet(ENCRYPTION_KEY)


# GET THE API CREDENTIALS
@api_bp.route('/token-generate')
@login_required
def generate_token():
    tz = pytz.timezone("America/Bogota")
    user_id = current_user.user_id
    user = db.get_or_404(User, user_id)
    
    if not user:
        logger.info(f"User not found: {user_id}")
        return jsonify({'message': 'User not found'}), 404
    
    # Generar el api_key y cifrarlo
    public_api_key = secrets.token_urlsafe(15)
    user.public_api_key = public_api_key
    user.public_api_key_expires = datetime.datetime.now(tz=tz) + datetime.timedelta(days=90)
    
    secret_api_key = secrets.token_urlsafe(15)
    encrypted_api_key = cipher_suite.encrypt(secret_api_key.encode('utf-8')).decode('utf-8')
    user.secret_api_key = encrypted_api_key
    user.secret_api_key_expires = datetime.datetime.now(tz=tz) + datetime.timedelta(days=90)
    
    if user.is_admin:
        admin_api_key = secrets.token_urlsafe(32)
        encrypted_admin_api= cipher_suite.encrypt(admin_api_key.encode('utf-8')).decode('utf-8')
        user.admin_api_key= encrypted_admin_api
        
    
    db.session.commit()
    
    if user.is_admin:
        logger.info(f"Admin {user.username} created api credentials")
        return jsonify({'admin_api_key': admin_api_key, 
                        'public_api_key': public_api_key,
                        'secret_api_key':secret_api_key})
    else:
        logger.info(f"User {user.username} created api credentials")
        return jsonify({'public_api_key': public_api_key,
                        'secret_api_key':secret_api_key})




