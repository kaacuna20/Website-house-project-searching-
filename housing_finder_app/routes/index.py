from flask import Blueprint, render_template, request, redirect, flash, url_for
from housing_finder_app.models import Project
from housing_finder_app.models import db
from sqlalchemy import or_


index_bp = Blueprint('index', __name__)


# MAIN SECTION
@index_bp.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Input in homepage
        projects_by_item = request.form["search"]
        # Projects filtered by location, city and company
        filtered_projects = Project.query.filter(or_(Project.location == projects_by_item.title(),
                                                     Project.company == projects_by_item.upper(),
                                                     Project.city == projects_by_item.title())).all()

        if filtered_projects:
            return render_template("all_projects.html", all_projects=filtered_projects)

        if projects_by_item == "todos":
            all_projects = db.session.execute(db.select(Project)).scalars().all()
            return render_template("all_projects.html", all_projects=all_projects)

        else:
            flash("No se encontraron resultados a su búsqueda!")
            return redirect(url_for('index.home'))

    return render_template("index.html")


# ABOUT SECTION
@index_bp.route("/about")
def about():
    return render_template("about.html")