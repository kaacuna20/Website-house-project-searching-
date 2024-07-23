from flask import Blueprint, render_template, request, redirect, flash, url_for


index_bp = Blueprint('index', __name__)


# MAIN SECTION
@index_bp.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Input in homepage
        projects_by_item = request.form["search"]
        
        # Redirect to the get_all_projects view with the search term as a query parameter
        if projects_by_item:
            return redirect(url_for('project.get_all_projects', search=projects_by_item))

        if projects_by_item == "todos":
            return redirect(url_for('project.get_all_projects'))

        else:
            flash("No se encontraron resultados a su búsqueda!")
            return redirect(url_for('index.home'))

    return render_template("index.html")


# ABOUT SECTION
@index_bp.route("/about")
def about():
    return render_template("about.html")