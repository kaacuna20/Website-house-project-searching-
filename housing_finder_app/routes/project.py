from flask import Blueprint, render_template,redirect, url_for, flash
from flask_login import current_user
from housing_finder_app.models import Project, Comment
from housing_finder_app.models import db
from housing_finder_app.auth.forms import CommentForm

project_bp = Blueprint('project', __name__)


# SHOW ALL PROJECTS *
@project_bp.route('/projects')
def get_all_projects():
    projects = db.session.execute(db.select(Project)).scalars().all()
    return render_template("all_projects.html", all_projects=projects, current_user=current_user)


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
            text=comment_form.comment_text.data,
            comment_user=current_user,
            parent_project=requested_project
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("project.html", project=requested_project, current_user=current_user, form=comment_form)
