from flask import Blueprint, render_template,redirect, url_for, flash, request
from flask_login import current_user
from app.models import Project, Comment
from app.models import db
from app.auth.forms import CommentForm
from sqlalchemy import or_, func
from app.utils.helpers import normalize_text

project_bp = Blueprint('project', __name__)


# SHOW ALL PROJECTS *
@project_bp.route('/projects')
def get_all_projects():
    search_term = request.args.get('search', default=None)
    page = request.args.get('page', default=1, type=int)
    per_page = 12
    
    if search_term and search_term.lower() != "todos":
        normalized_search_term = normalize_text(search_term)
        search_pattern = f"%{normalized_search_term}%"
        projects = Project.query.filter(
            or_(
                func.lower(Project.location).ilike(search_pattern),
                func.lower(Project.company).ilike(search_pattern),
                func.lower(Project.name).ilike(search_pattern),
                func.lower(Project.city).ilike(search_pattern)
            )
        ).all()
    else:
        projects = db.session.execute(db.select(Project)).scalars().all()

    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(projects) + per_page - 1) // per_page
    item_on_page = projects[start:end]

    return render_template("all_projects.html",
                           all_projects=item_on_page, 
                           total_pages=total_pages,
                           page=page, 
                           search_term=search_term,
                           current_user=current_user
                        )


# SHOW FEATURES INDIVIDUAL PROJECT SECTION
@project_bp.route("/<slug>", methods=["GET", "POST"])
def show_project(slug):
    requested_project = db.session.execute(db.select(Project).where(Project.slug == slug)).scalar()
    # Adding the CommentForm to the route
    comment_form = CommentForm()
    # Only allow logged-in users to comment on projects
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Debes iniciar sección para poder comentar.")
            return redirect(url_for("user.login"))

        new_comment = Comment(
            comment=comment_form.comment_text.data,
            comment_user=current_user,
            parent_project=requested_project
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("project.html", 
                           project=requested_project, 
                           current_user=current_user,
                           form=comment_form
                        )
