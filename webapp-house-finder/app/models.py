from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime, Float, CheckConstraint
from flask_login import UserMixin
from slugify import slugify


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Project(db.Model):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    logo: Mapped[str] = mapped_column(String(250), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    city: Mapped[str] = mapped_column(String(250), nullable=False)
    company: Mapped[str] = mapped_column(String(250), nullable=False)
    address: Mapped[str] = mapped_column(String(250), nullable=False)
    url_map: Mapped[str] = mapped_column(String(500), nullable=False)
    contact: Mapped[str] = mapped_column(String(250), nullable=False)
    area: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    url_website: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(250), unique=True, nullable=False, index=True)
    # Parent relationship to the comments
    comments = relationship("Comment", back_populates="parent_project")
    # Relationship with User table (many-to-many)
    saved_by = db.relationship('User', secondary='project_users',
                               backref=db.backref('saved_projects', lazy='dynamic'))

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.slug = slugify(self.name)  # Generate slug on object creation
        super(Project, self).__init__(*args, **kwargs)  # Call parent constructor

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, lower=True)
        super().save(*args, **kwargs)  # Call parent save method

    def __repr__(self):
        return f'<Project {self.name}>'

    __table_args__ = (
        CheckConstraint('price >= :0', name='min_integer_check'),
        CheckConstraint('area >= :0', name='min_float_check'),
    )


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
    photo: Mapped[str] = mapped_column(String(200), nullable=False)
    api_key: Mapped[str] = mapped_column(String(200), unique=True, nullable=True)
    api_key_expires: Mapped[str] = mapped_column(DateTime, nullable=True)
    token_secret: Mapped[str] = mapped_column(String(200), unique=True, nullable=True)
    token_secret_expires: Mapped[str] = mapped_column(DateTime, nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    # Parent relationship: "comment_user" refers to the comment_user property in the Comment class.
    comments = relationship("Comment", back_populates="comment_user")

    def __repr__(self):
        return f'<User {self.username}>'


# Create a table for the relationship many to many  between User and Project class
class ProjectUser(db.Model):
    __tablename__ = 'project_users'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)

    # Additional columns to store project-specific data for the user
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
    projectc_id: Mapped[str] = mapped_column(Integer, db.ForeignKey("projects.id" ,ondelete='CASCADE'), nullable=True)
    parent_project = relationship("Project", back_populates="comments")