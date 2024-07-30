from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, CheckConstraint, Text
from sqlalchemy.ext.declarative import declarative_base
from slugify import slugify

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(200))
    username = Column(String(100))
    name = Column(String(100))
    lastname = Column(String(100))
    city = Column(String(100))
    photo = Column(String(200), nullable=True)
    public_api_key = Column(String(200), unique=True, nullable=True, index=True)
    public_api_key_expires = Column(DateTime, nullable=True)
    secret_api_key = Column(String(500), nullable=True)
    secret_api_key_expires = Column(DateTime, nullable=True)
    admin_api_key = Column(String(500), nullable=True)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    logo = Column(String(250), nullable=False)
    location = Column(String(150), nullable=False)
    city = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    contact = Column(String(50), nullable=False)
    area = Column(Float, nullable=False)
    price = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False)
    img_url = Column(String(300), nullable=False)
    description = Column(Text, nullable=False)
    url_website = Column(String(250), unique=True, nullable=False)
    slug = Column(String(250), unique=True, nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
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