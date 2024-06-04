from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app.models import User, Project, ProjectUser
from app.models import db
from app.auth.forms import ChangePasswordForm

profile_bp = Blueprint('profile', __name__)


# SAVE PROJECT BY USER
@profile_bp.route("/<int:user_id>/<int:project_id>")
@login_required
def save_project_user(user_id, project_id):
    user = db.get_or_404(User, user_id)
    project = db.get_or_404(Project, project_id)
    user.saved_projects.append(project)
    db.session.commit()
    return redirect(url_for("profile.user_projects", user_id=user_id))


# DELETE PROJECT SAVED BY USER
@profile_bp.route("/delete/<int:user_id>/<int:project_id>")
@login_required
def delete_project_user(user_id, project_id):
    db.session.query(ProjectUser).filter_by(user_id=user_id, project_id=project_id).delete()
    db.session.commit()
    return redirect(url_for("profile.user_projects", user_id=user_id))


# SHOW SAVED PROJECTS BY USER
@profile_bp.route("/user")
@login_required
def user_projects():
    user_id = current_user.id
    user = User.query.get(user_id)
    saved_projects = user.saved_projects.all()
    return render_template("projects_by_user.html", my_projects=saved_projects, current_user=current_user)


# EDIT PROFILE USER SECTION
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@profile_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_id = current_user.id
    user_db = db.get_or_404(User, user_id)
    # edit profile section
    if request.method == 'POST':
        # update the profile photo by user
        uploaded_file = request.files["image_file"]
        # Verify if update any file
        if not uploaded_file:
            flash("No se ha cargado el archivo.")
            return redirect(url_for('profile.edit_profile', current_user=current_user))
        # Verify if extension of file is valid
        elif not allowed_file(uploaded_file.filename):
            flash("Archivo no valido.")
            return redirect(url_for('profile.edit_profile', current_user=current_user))
        # Update the photo on user profile
        elif uploaded_file and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            # store the file inside the static files
            uploaded_file.save(f"app/static/images/img-profile/{filename}")
            # save and add the next path in database column 'photo'
            user_db.photo = f"static/images/img-profile/{filename}"
            db.session.commit()
            return redirect(url_for('profile.edit_profile', current_user=current_user))
    return render_template("user_profile.html", current_user=current_user)


# CHANGE PASSWORD SECTION
@profile_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    user_id = current_user.id
    user_db = db.get_or_404(User, user_id)
    # change password section
    change_password_section = ChangePasswordForm()
    if change_password_section.validate_on_submit():
        written_password = change_password_section.current_password.data
        # Verify if the current password is right
        if not check_password_hash(user_db.password, written_password):
            flash('Contraseña incorrecta, por favor trate de nuevo.')
            return redirect(url_for('profile.change_password', current_user=current_user))
        # Verify if the next password are equal
        if change_password_section.new_password.data != change_password_section.verificate_password.data:
            flash('Las contraseñas no son iguales.')
            return redirect(url_for('profile.change_password', current_user=current_user))
        # update the next password, logout section and user must login with the new password
        else:
            new_password = generate_password_hash(
                password=change_password_section.new_password.data,
                method="pbkdf2:sha256",
                salt_length=8
            )
            user_db.password = new_password
            db.session.commit()
            logout_user()
            return redirect(url_for('user.login'))
    return render_template("password_section.html", current_user=current_user, form=change_password_section)