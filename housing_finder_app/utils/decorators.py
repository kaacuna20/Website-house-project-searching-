from flask import request, jsonify
import jwt
from functools import wraps
from housing_finder_app.models import User
import os

SECRET_KEY = os.getenv("SECRET_KEY")


# DECORATORS FUNCTIONS
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get("api_key")
        # Verify if current user has generated a apikey
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        # Authenticate if apikey's user is valid
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except Exception:
            return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key or refresh it."}), 403
        return f(*args, **kwargs)
    return decorated


def only_admi(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get("api_key")
        # On database, the first user_id correspond to administer
        admi = User.query.filter(User.is_admin == True).first()
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        # Authenticate if the apikey correspond to administer apikey
        if not admi:
            return jsonify({'message': 'You are not the administrator, you are not authorized!'}), 403
        else:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return f(*args, **kwargs)
    return decorated
