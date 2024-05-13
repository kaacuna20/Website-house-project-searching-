import os
from dotenv import load_dotenv

load_dotenv(".env")
# Define the base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# MySQL database configuration
#SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI") + os.path.join(BASE_DIR, os.getenv("DATABASE") )

# Secret key for session management and CSRF protection
#SECRET_KEY = os.getenv("SECRET_KEY")

# Database URI (e.g., SQLite, PostgreSQL, etc.)
#SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
#SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids overhead

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids overhead

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.getenv("ADMINISTER_EMAIL")
    MAIL_PASSWORD = os.getenv("APP_PASSWORD_EMAIL")
    DONT_REPLY_FROM_EMAIL = os.getenv("ADMINISTER_EMAIL")
    ADMINS = (os.getenv("ADMINISTER_EMAIL"),)
    MAIL_USE_TLS = True


class ProductionConfig(Config):
    pass
