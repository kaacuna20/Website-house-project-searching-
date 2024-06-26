from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from slugify import slugify

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    username = Column(String(100), unique=True)
    name = Column(String(100))
    lastname = Column(String(100))
    city = Column(String(100))
    photo = Column(String(200), nullable=False)
    api_key = Column(String(200), unique=True, nullable=True)
    api_key_expires = Column(DateTime, nullable=True)
    token_secret = Column(String(500), nullable=True)
    token_secret_expires = Column(DateTime, nullable=True)
    is_admin = Column(Boolean, default=False)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), unique=True, nullable=False)
    logo = Column(String(250), nullable=False)
    location = Column(String(250), nullable=False)
    city = Column(String(250), nullable=False)
    company = Column(String(250), nullable=False)
    address = Column(String(250), nullable=False)
    url_map = Column(String(500), nullable=False)
    contact = Column(String(250), nullable=False)
    area = Column(Float, nullable=False)
    price = Column(Integer, nullable=False)
    type = Column(String(250), nullable=False)
    img_url = Column(String(500), nullable=False)
    description = Column(String, nullable=False)
    url_website = Column(String(250), unique=True, nullable=False)
    slug = Column(String(250), unique=True, nullable=False, index=True)

    def to_dict(self):
        # Loop through each column in the data record in a dictionary
        # where the key is the name of the column
        # and the value is the value of the column
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    
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