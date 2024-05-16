import os
from dotenv import load_dotenv

load_dotenv(".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids overhead


class DevelopmentConfig(Config):
    """Development configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.getenv("ADMINISTER_EMAIL")
    MAIL_PASSWORD = os.getenv("APP_PASSWORD_EMAIL")
    DONT_REPLY_FROM_EMAIL = os.getenv("ADMINISTER_EMAIL")
    ADMINS = (os.getenv("ADMINISTER_EMAIL"),)
    MAIL_USE_TLS = True


class TestingConfig(Config):
    """Testing configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids overhead
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI_TEST")
    # Disable CSRF protection for testing
    WTF_CSRF_ENABLED: False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.getenv("ADMINISTER_EMAIL")
    MAIL_PASSWORD = os.getenv("APP_PASSWORD_EMAIL")
    DONT_REPLY_FROM_EMAIL = os.getenv("ADMINISTER_EMAIL")
    ADMINS = (os.getenv("ADMINISTER_EMAIL"),)
    MAIL_USE_TLS = True


class ProductionConfig(Config):
    pass
