from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
import jwt
import datetime
import pytz
from functools import wraps
from housing_finder_app.models import User, Project
from housing_finder_app.models import db
import os

SECRET_KEY=os.getenv("SECRET_KEY")

api_bp = Blueprint('api', __name__, static_folder='static', static_url_path='/static')




# DECORATORS FUNCTION
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
        admi = db.session.execute(db.select(User).where(User.is_admin == True)).scalar()
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        # Authenticate if the apikey correspond to administer apikey
        if not token == admi.api_key:
            return jsonify({'message': 'You are not the administrator, you are not authorized!'}), 403
        else:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return f(*args, **kwargs)
    return decorated





@api_bp.route('/token/generate')
@login_required
def generate_token():
    # set the zone
    tz = pytz.timezone("America/Bogota")
    user_id = current_user.id
    user = db.get_or_404(User, user_id)
    # Verify if user is registered in database
    if not user:
        return jsonify({'message': 'User not found'}), 404
    # Generate the apikey
    token = jwt.encode({
        'user': user.username,
        'exp': datetime.datetime.now(tz=tz) + datetime.timedelta(days=90)
    }, SECRET_KEY, algorithm="HS256")
    # store the apikey in database with current user
    user.api_key = token
    user.api_key_expires = datetime.datetime.now(tz=tz) + datetime.timedelta(days=90)
    db.session.commit()
    # Show to the user the apikey
    return jsonify({'api_key': token})


# HTTP GET - Read Record
@api_bp.route("/location")
@token_required
def project_by_location():
    # search by location
    query_loc = request.args.get("loc").title()
    locate_project = db.session.execute(db.select(Project).where(Project.location == query_loc)).scalars().all()
    if locate_project:
        return jsonify(projects=[project.to_dict() for project in locate_project])
    else:
        return jsonify(error={"Not found": "Sorry, we don't have a project at that location."}), 404


@api_bp.route("/city")
@token_required
def project_by_city():
    # search by city
    query_city = request.args.get("city").title()
    locate_project = db.session.execute(db.select(Project).where(Project.city == query_city)).scalars().all()
    if locate_project:
        return jsonify(projects=[project.to_dict() for project in locate_project])
    else:
        return jsonify(error={"Not found": "Sorry, we don't have a project at that location."}), 404


# HTTP POST - Create Record
@api_bp.route("/add", methods=["POST"])
@token_required
def post_new_project():
    try:
        new_project = Project(
            name=request.args.get("name").title(),
            logo=request.args.get("logo").lower(),
            location=request.args.get("location").title(),
            city=request.args.get("city").title(),
            company=request.args.get("company").upper(),
            address=request.args.get("address").title(),
            url_map=request.args.get("url_map").lower(),
            contact=request.args.get("contact").lower(),
            area=request.args.get("area").lower(),
            price=request.args.get("price").lower(),
            type=request.args.get("type").upper(),
            img_url=request.args.get("img_url").lower(),
            description=request.args.get("description"),
            url_website=request.args.get("url_website").lower(),
        )
        db.session.add(new_project)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new project."}), 200
    except Exception as ex:
        print(ex)
        return jsonify(
            error={"Internal Server Error": "Sorry, but this project already exist on the database"
                                            " or there is an empty  or wrong item."}), 500


# HTTP PUT/PATCH - Update Record
@api_bp.route("/update-price", methods=["PATCH"])
@token_required
def update_new_project_price():
    # Update a new price by project
    project_id = int(request.args.get("project_id"))
    price_to_update = db.get_or_404(Project, project_id)
    if price_to_update:
        price_to_update.price = request.args.get("new_price")
        db.session.commit()
        return jsonify(response={"success": "Successfully update the price."}), 200
    else:
        return jsonify(error={"Not found": "Sorry a project with that id was not found in the database."}), 404


# HTTP DELETE - Delete Record
@api_bp.route("/project-closed", methods=["DELETE"])
@only_admi
def delete_project():
    # Delete a record (only allowed by administer)
    project_id = int(request.args.get("project_id"))
    try:
        project_to_delete = db.get_or_404(Project, project_id)
        db.session.delete(project_to_delete)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the project from the database."}), 200
    except Exception:
        return jsonify(error={"Not Found": "Sorry a project with that id was not found in the database."}), 404