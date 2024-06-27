from flask import Blueprint, render_template
from flask_login import login_required, current_user
from os import environ

api_doc_bp = Blueprint('api_doc', __name__)


# API DOCUMENTATION SECTION
@api_doc_bp.route("/api-documentation")
def documentation_api():
    server = environ.get('SERVER_NAME')
    return render_template("documentation_api.html", server=server)


@api_doc_bp.route("/api_key")
@login_required
def get_api_key():
    return render_template("api_key.html", current_user=current_user)