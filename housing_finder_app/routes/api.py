from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import jwt
import datetime
import pytz
from housing_finder_app.utils.decorators import token_required, only_admi
from housing_finder_app.models import User, Project
from housing_finder_app.models import db
import os

SECRET_KEY = os.getenv("SECRET_KEY")

api_bp = Blueprint('api', __name__)


@api_bp.route('/token-generate')
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
        return jsonify(projects=[project.to_dict() for project in locate_project]), 200
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
        return jsonify(error={"Not found": "Sorry, we don't have a project at that city."}), 404


@api_bp.route("/company")
@token_required
def project_by_company():
    # search by location
    query_company = request.args.get("company").upper()
    locate_project = db.session.execute(db.select(Project).where(Project.company == query_company)).scalars().all()

    if locate_project:
        return jsonify(projects=[project.to_dict() for project in locate_project]), 200
    else:
        return jsonify(error={"Not found": "Sorry, we don't have a projects at that company."}), 404


@api_bp.route("/project-details")
@token_required
def project():
    # search by location
    project_id = int(request.args.get("project_id"))
    try:
        locate_project = db.get_or_404(Project, project_id)
        return jsonify({f"{locate_project.name}": locate_project.to_dict()}), 200
    except Exception:
        return jsonify(error={"Not found": "Sorry, we don't have that project."}), 404


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
            area=request.args.get("area"),
            price=request.args.get("price"),
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

    try:
        price_to_update = db.get_or_404(Project, project_id)
        price_to_update.price = request.args.get("new_price")
        db.session.commit()
        return jsonify(response={"success": "Successfully update the price."}), 200
    except Exception:
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