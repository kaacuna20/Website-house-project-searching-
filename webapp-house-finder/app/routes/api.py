from flask import Blueprint, jsonify
from flask_login import login_required, current_user
import jwt
import datetime
import pytz
from app.models import User
from app.models import db
from os import environ
import secrets

SECRET_KEY = environ.get('SECRET_APP_KEY')

api_bp = Blueprint('api', __name__)


# GET THE API CREDENTIALS
@api_bp.route('/token-generate')
@login_required
def generate_token():
    # set the zone
    tz = pytz.timezone("America/Bogota")
    user_id = current_user.user_id
    user = db.get_or_404(User, user_id)
    # Verify if user is registered in database
    if not user:
        return jsonify({'message': 'User not found'}), 404
    # Generate the apikey

    public_api_key = secrets.token_urlsafe(15)
    user.api_key = public_api_key
    user.api_key_expires = datetime.datetime.now(tz=tz) + datetime.timedelta(days=90)
    db.session.commit()

    # Generate the admin token just for admin
    if user.is_admin:
        admin_token = str(secrets.randbelow(10**25))
        user.token_secret = admin_token
        user.token_secret_expires = datetime.datetime.now(tz=tz) + datetime.timedelta(days=90)
        db.session.commit()
        # Show to the user the apikey and token
        return jsonify({'admin_token': admin_token, 'api_key': public_api_key})

    else:
        # Show to the user the apikey
        return jsonify({'api_key': public_api_key})

