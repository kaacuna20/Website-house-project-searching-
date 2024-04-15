from flask import Flask, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import smtplib
import jwt
from secrets import token_urlsafe
from flask_ckeditor import CKEditor
from functools import wraps
from forms import LoginForm, RegisterForm, CommentForm, ChangePasswordForm # export the form's class
import datetime
import pytz
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# Create bootstrap from flask
bootstrap = Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Set login view for unauthorized access

# Create ckeditor from flask
ckeditor = CKEditor(app)


# User loader callback for Flask-Login (fetches user from database)
@login_manager.user_loader
def load_user(user_id):
    # Fetch user data from database or other source
    return User.query.get(user_id)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES
# Create a Project table for all features of house project
class Project(db.Model):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    logo: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    city: Mapped[str] = mapped_column(String(250), nullable=False)
    company: Mapped[str] = mapped_column(String(250), nullable=False)
    address: Mapped[str] = mapped_column(String(250), nullable=False)
    url_map: Mapped[str] = mapped_column(String(250), nullable=False)
    address_sale: Mapped[str] = mapped_column(String(250), nullable=False)
    contact: Mapped[str] = mapped_column(String(250), nullable=False)
    stratum_city: Mapped[str] = mapped_column(String(250), nullable=False)
    area: Mapped[str] = mapped_column(String(250), nullable=False)
    price: Mapped[str] = mapped_column(String(250), nullable=False)
    type: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    url_website: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    # Parent relationship to the comments
    comments = relationship("Comment", back_populates="parent_project")
    # Relationship with User table (many-to-many)
    saved_by = db.relationship('User', secondary='project_users',
                               backref=db.backref('saved_projects', lazy='dynamic'))

    def __repr__(self):
        return f'<Project {self.name}>'

    def to_dict(self):
        # Loop through each column in the data record in a dictionary
        # where the key is the name of the column
        # and the value is the value of the column
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# Create a User table for all your registered users
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    lastname: Mapped[str] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(100))
    photo: Mapped[str] = mapped_column(String, nullable=False)
    api_key: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    api_key_expires: Mapped[str] = mapped_column(DateTime, nullable=True)
    # Parent relationship: "comment_user" refers to the comment_user property in the Comment class.
    comments = relationship("Comment", back_populates="comment_user")

    def __repr__(self):
        return f'<User {self.username}>'


# Create a table for the relationship many to many  between User and Project class
class ProjectUser(db.Model):
    __tablename__ = 'project_users'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)

    # Additional columns to store project-specific data for the user (optional)

    def __repr__(self):
        return f'<ProjectUser user_id={self.user_id}, project_id={self.project_id}>'


# Create a table for the comments on the individual project
class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    # Child relationship:"users.id" The users refers to the tablename of the User class.
    # "comments" refers to the comments property in the User class.
    userc_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    comment_user = relationship("User", back_populates="comments")
    # Child Relationship to the BlogPosts
    projectc_id: Mapped[str] = mapped_column(Integer, db.ForeignKey("projects.id"))
    parent_project = relationship("Project", back_populates="comments")


with app.app_context():
    db.create_all()


# MAIN SECTION
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Input in homepage
        projects_by_item = request.form["search"].title()
        # Projects filtered by location
        projects_by_location = db.session.execute(
            db.select(Project).where(Project.location == projects_by_item)).scalars().all()
        # Projects filtered by city
        projects_by_city = db.session.execute(
            db.select(Project).where(Project.city == projects_by_item)).scalars().all()
        # Projects filtered by company
        project_by_company = db.session.execute(
            db.select(Project).where(Project.company == projects_by_item)).scalars().all()
        if projects_by_item == "Todos":
            all_projects = db.session.execute(db.select(Project)).scalars().all()
            return render_template("all_projects.html", all_projects=all_projects)
        elif projects_by_location:
            return render_template("all_projects.html", all_projects=projects_by_location)
        elif projects_by_city:
            return render_template("all_projects.html", all_projects=projects_by_city)
        elif project_by_company:
            return render_template("all_projects.html", all_projects=project_by_company)
        else:
            flash("No se encontraron resultados a su búsqueda!")
            return redirect(url_for('home'))
    return render_template("index.html")


# REGISTER USER SECTION
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user email is already present in the database.
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if user:
            # User already exists
            flash("Ya estas registrado, ve e inicia sección!")
            return redirect(url_for('login'))

        new_user = User(
            name=form.name.data,
            lastname=form.lastname.data,
            city=form.city.data,
            email=form.email.data,
            password=generate_password_hash(
                password=form.password.data,
                method="pbkdf2:sha256",
                salt_length=8
            ),
            username=form.username.data,
            photo="static/images/profile.png"
        )
        db.session.add(new_user)
        db.session.commit()
        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html", form=form, current_user=current_user)


# LOGIN USER SECTION
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        # Email doesn't exist
        if not user:
            flash("El correo no existe, por favor trate de nuevo.")
            return redirect(url_for('register'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Contraseña incorrecta, por favor trate de nuevo.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html", form=form, current_user=current_user)


# SAVE PROJECT BY USER
@app.route("/<int:user_id>/<int:project_id>")
def save_project_user(user_id, project_id):
    user = db.get_or_404(User, user_id)
    project = db.get_or_404(Project, project_id)
    user.saved_projects.append(project)
    db.session.commit()
    return redirect(url_for("user_projects", user_id=user_id))


@app.route("/delete/<int:user_id>/<int:project_id>")
def delete_project_user(user_id, project_id):
    db.session.query(ProjectUser).filter_by(user_id=user_id, project_id=project_id).delete()
    db.session.commit()
    return redirect(url_for("user_projects", user_id=user_id))


@app.route("/user")
@login_required
def user_projects():
    user_id = current_user.id
    user = User.query.get(user_id)
    saved_projects = user.saved_projects.all()
    return render_template("projects_by_user.html", my_projects=saved_projects, current_user=current_user)


# LOGOUT USER SECTION
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# EDIT PROFILE USER SECTION
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/profile', methods=['GET', 'POST'])
def edit_profile():
    user_id = current_user.id
    user_db = db.get_or_404(User, user_id)
    # edit profile section
    if request.method == 'POST':
        uploaded_file = request.files["image_file"]
        if not uploaded_file:
            flash("No se ha cargado el archivo.")
            return redirect(url_for('edit_profile', current_user=current_user))
        elif not allowed_file(uploaded_file.filename):
            flash("Archivo no valido.")
            return redirect(url_for('edit_profile', current_user=current_user))
        elif uploaded_file and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(f"static/images/img_profile/{filename}")
            user_db.photo = f"static/images/img_profile/{filename}"
            db.session.commit()
            return redirect(url_for('edit_profile', current_user=current_user))
    return render_template("user_profile.html", current_user=current_user)


# CHANGE PASSWORD SECTION
@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    user_id = current_user.id
    user_db = db.get_or_404(User, user_id)
    # change password section
    change_passwd_section = ChangePasswordForm()
    if change_passwd_section.validate_on_submit():
        written_password = change_passwd_section.current_password.data
        if not check_password_hash(user_db.password, written_password):
            flash('Contraseña incorrecta, por favor trate de nuevo.')
            return redirect(url_for('change_password', current_user=current_user))
        if change_passwd_section.new_password.data != change_passwd_section.verificate_password.data:
            flash('Las contraseñas no son iguales.')
            return redirect(url_for('change_password', current_user=current_user))
        else:
            new_password = generate_password_hash(
                password=change_passwd_section.new_password.data,
                method="pbkdf2:sha256",
                salt_length=8
            )
            user_db.password = new_password
            db.session.commit()
            logout_user()
            return redirect(url_for('login'))
    return render_template("password_section.html", current_user=current_user, form=change_passwd_section)


# FORGOT PASSWORD
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == "POST":
        user = db.session.execute(db.select(User).where(User.email == request.form["email"].lower())).scalar()
        # Verify email correspond to a user registered
        if not user:
            flash("El correo no se registra en nuestra base de datos, por favor trate de nuevo.")
            return redirect(url_for('forgot_password'))

        # generate a new and temporal password
        temporal_password = f"Tu nueva contraseña es: {token_urlsafe(8)}"
        # store this password on database
        new_password = generate_password_hash(
            password=temporal_password,
            method="pbkdf2:sha256",
            salt_length=8
            )
        user.password = new_password
        db.session.commit()
        # send the password for email
        # split the email after "@" to get the host of email
        stmp = request.form["email"].lower().split("@")[1]
        # create a dictionary to know what smtp.host correspond the email
        host_emails = {
            "gmail.com": "smtp.gmail.com",
            "hotmail.com": "smtp.live.com"
        }
        # put the right location host of email
        connection = smtplib.SMTP(host_emails[stmp])
        connection.starttls()
        connection.login(user="casaacuna47@gmail.com", password="cwieaggngjpanpet")
        connection.sendmail(
            from_addr="casaacuna47@gmail.com",
            to_addrs=request.form["email"].lower(),
            msg=temporal_password
        )
        connection.close()
        return redirect(url_for('login'))
    return render_template("forgot_password.html")


# ABOUT SECTION
@app.route("/about")
def about():
    return render_template("about.html")


# SHOW ALL PROJECTS *
@app.route('/projects')
def get_all_projects():
    projects = db.session.execute(db.select(Project)).scalars().all()
    return render_template("all_projects.html", all_projects=projects, current_user=current_user)


# SHOW FEATURES INDIVIDUAL PROJECT SECTION
@app.route("/<int:project_id>", methods=["GET", "POST"])
def show_project(project_id):
    requested_project = db.get_or_404(Project, project_id)
    # Adding the CommentForm to the route
    comment_form = CommentForm()
    # Only allow logged-in users to comment on projects
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Debes iniciar sección para poder comentar.")
            return redirect(url_for("login"))

        new_comment = Comment(
            text=comment_form.comment_text.data,
            comment_user=current_user,
            parent_project=requested_project
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("project.html", project=requested_project, current_user=current_user, form=comment_form)


# API DOCUMENTATION SECTION
@app.route("/api")
def documentation_api():
    return render_template("documentation_api.html")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get("api_key")
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except Exception:
            return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key or refresh it."}), 403
        return f(*args, **kwargs)
    return decorated


@app.route("/api_key")
def get_api_key():
    return render_template("api_key.html", current_user=current_user)


@app.route('/api/token/generate')
def generate_token():
    tz = pytz.timezone("America/Bogota")
    user_id = current_user.id
    user = db.get_or_404(User, user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    token = jwt.encode({
        'user': user.username,
        'exp': datetime.datetime.now(tz=tz) + datetime.timedelta(days=90)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    user.api_key = token
    user.api_key_expires = datetime.datetime.now(tz=tz) + datetime.timedelta(days=90)
    db.session.commit()

    return jsonify({'api_key': token})


# HTTP GET - Read Record
@app.route("/location")
@token_required
def project_by_location():
    # search by location
    query_loc = request.args.get("loc").title()
    locate_project = db.session.execute(db.select(Project).where(Project.location == query_loc)).scalars().all()
    if locate_project:
        return jsonify(projects=[project.to_dict() for project in locate_project])
    else:
        return jsonify(error={"Not found": "Sorry, we don't have a project at that location."}), 404


@app.route("/city")
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
@app.route("/add", methods=["POST"])
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
            address_sale=request.args.get("address_sale").title(),
            contact=request.args.get("contact").lower(),
            stratum_city=request.args.get("stratum").title(),
            area=request.args.get("area").lower(),
            price=request.args.get("price").lower(),
            type=request.args.get("type").upper(),
            img_url=request.args.get("img_url").lower(),
            description=request.args.get("description"),
            url_website=request.args.get("url_website").lower(),
        )
        db.session.add(new_project)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new project."})
    except Exception:
        return jsonify(
            error={"Internal Server Error": "Sorry, but this project already exist on the database."}), 500


# HTTP PUT/PATCH - Update Record
@app.route("/update-price", methods=["PATCH"])
@token_required
def update_new_project_price():
    project_id = int(request.args.get("project_id"))
    price_to_update = db.get_or_404(Project, project_id)
    if price_to_update:
        price_to_update.price = request.args.get("new_price")
        db.session.commit()
        return jsonify(response={"success": "Successfully update the price."}), 200
    else:
        return jsonify(error={"Not found": "Sorry a cafe with that id was not found in the database."}), 404


# HTTP DELETE - Delete Record
@app.route("/project-closed", methods=["DELETE"])
@token_required
def delete_project():
    project_id = int(request.args.get("project_id"))
    try:
        project_to_delete = db.get_or_404(Project, project_id)
        db.session.delete(project_to_delete)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the project from the database."}), 200
    except Exception:
        return jsonify(error={"Not Found": "Sorry a project with that id was not found in the database."}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5002)
