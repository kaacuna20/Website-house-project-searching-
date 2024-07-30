from flask import Blueprint, render_template
from flask_login import login_required, current_user
from cryptography.fernet import Fernet
from os import environ
from app.logs_system.log import Logger

logger = Logger()

api_doc_bp = Blueprint('api_doc', __name__)

ENCRYPTION_KEY = environ.get('ENCRYPTION_KEY')

cipher_suite = Fernet(ENCRYPTION_KEY)

# API DOCUMENTATION SECTION
@api_doc_bp.route("/api_key")
@login_required
def get_api_key():
    decrypted_secret_api_key = None
    decrypted_admin_api_key = None

    # Check and decrypt the secret API key if present
    if current_user.secret_api_key:
        try:
            secret_api_key = current_user.secret_api_key
            if isinstance(secret_api_key, str):
                secret_api_key = secret_api_key.encode('utf-8')  # Convert to bytes if it's a string
            decrypted_secret_api_key = cipher_suite.decrypt(secret_api_key).decode('utf-8')
        except Exception as e:
            logger.error(f"Error decrypting secret_api_key: {e}")
    print(current_user.username)
    print(current_user.secret_api_key)
    # Check and decrypt the admin API key if the user is an admin
    if current_user.is_admin and current_user.admin_api_key:
        try:
            admin_api_key = current_user.admin_api_key
            if isinstance(admin_api_key, str):
                admin_api_key = admin_api_key.encode('utf-8')  # Convert to bytes if it's a string
            decrypted_admin_api_key = cipher_suite.decrypt(admin_api_key).decode('utf-8')
        except Exception as e:
            logger.error(f"Error decrypting admin_api_key: {e}")

    return render_template("api_key.html", 
                           secret_api_key=decrypted_secret_api_key,
                           public_api_key=current_user.public_api_key,  
                           admin_api_key=decrypted_admin_api_key,
                           current_user=current_user)




