from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text

app = Flask(__name__)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# Create bootstrap from flask
bootstrap = Bootstrap5(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES
class Project(db.Model):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    logo:  Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
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


# Create a User table for all your registered users
class User(db.Model):  # UserMixin,
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100))
    # Parent relationship: "comment_user" refers to the comment_user property in the Comment class.
    comments = relationship("Comment", back_populates="comment_user")

    def __repr__(self):
        return f'<User {self.username}>'


class ProjectUser(db.Model):
    __tablename__ = 'project_users'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)

    # Additional columns to store project-specific data for the user (optional)

    def __repr__(self):
        return f'<ProjectUser user_id={self.user_id}, project_id={self.project_id}>'


# Create a table for the comments on the blog posts
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
"""with app.app_context():
    new_project = Project(
        name="Mirador de Cienaga",
        location="Ciudad Mallorquín",
        logo="https://media1.amarilo.com.co/website/s3fs-public/proyectos/2023-09/37.%20LOGO%20MIRADOR%20DE%20LA%20CIENAGA.jpg",
        city="Puerto Colombia",
        company="AMARILO",
        address="Calle. 110 No.43 - 331, Manzana 13",
        url_map="https://www.google.com/maps/dir//11.006408,-74.842512",
        address_sale="Ediempresarial, Cra 53 #110 Esquina, Local 5",
        contact="3103157550",
        stratum_city="3",
        area="56",
        price="175.500.000",
        type="VIS",
        img_url="https://media1.amarilo.com.co/website/s3fs-public/proyectos/2023-07/mirador_de_la_cienaga_-_ciudad_mallorquin_apartamentos-en-barranquilla-amarilo-mirador-aprovecha-nuevos-aptos-a.jpeg",
        description="Mirador de la Ciénaga es un conjunto residencial de vivienda tipo Tope VIS (Vivienda de Interés Social) que se desarrolla en la Manzana Residencial 5 Lote 1 del Plan Parcial 'Ribera Mallorquín 'bicado en el municipio de Puerto Colombia.",
        url_website="https://amarilo.com.co/proyecto/mirador-cienaga-ciudad-mallorquin?utm_source=landing%20mallorquin&utm_medium=cpc"
    )
    db.session.add(new_project)
    db.session.commit()"""

# Create a form to register new users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    username = StringField("Usuario", validators=[DataRequired()])
    submit = SubmitField("Registrar")


# Create a form to login existing users
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Acceder")


# Create a form to add comments
class CommentForm(FlaskForm):
    comment_text = CKEditorField("Commentarios", validators=[DataRequired()])
    submit = SubmitField("Comentar")


class Search(FlaskForm):
    search_project = StringField("Buscar projecto por localidad, ciudad, o constructora, sino escribe 'todos'",
                                 validators=[DataRequired()])
    submit = SubmitField("Buscar")


@app.route("/", methods=["GET", "POST"])
def home():
    search = Search()
    if search.validate_on_submit():
        # Input in homepage
        projects_by_item = search.search_project.data
        # Projects filtered by location
        projects_by_location = db.session.execute(db.select(Project).where(Project.location == projects_by_item)).scalars().all()
        # Projects filtered by city
        projects_by_city = db.session.execute(db.select(Project).where(Project.city == projects_by_item)).scalars().all()
        # Projects filtered by company
        project_by_company = db.session.execute(db.select(Project).where(Project.company == projects_by_item)).scalars().all()
        if projects_by_item == "todos":
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
    return render_template("index.html", form=search)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for("home"))
    return render_template("register.html", form=form)  # , current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for("home"))
    return render_template("login.html", form=form)  # , current_user=current_user)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/projects')
def get_projects():
    projects = db.session.execute(db.select(Project)).scalars().all()
    return render_template("all_projects.html", all_projects=projects)  # , current_user=current_user)


@app.route("/<int:project_id>")
def show_project(project_id):
    requested_project = db.get_or_404(Project, project_id)
    return render_template("project.html", project=requested_project)#, current_user=current_user, form=comment_form)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
