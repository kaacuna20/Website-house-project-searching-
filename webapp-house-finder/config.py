from os import environ


class Config:
    SECRET_KEY = environ.get('SECRET_APP_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids overhead


class DevelopmentConfig(Config):
    """Development configuration."""
    SQLALCHEMY_DATABASE_URI = environ.get('DB_URL')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = environ.get('ADMINISTER_EMAIL')
    MAIL_PASSWORD = environ.get('APP_PASSWORD_EMAIL')
    DONT_REPLY_FROM_EMAIL =environ.get('ADMINISTER_EMAIL')
    ADMINS = (environ.get('ADMINISTER_EMAIL'),)
    MAIL_USE_TLS = True
    
    
class TestingConfig(Config):
    """Testing configuration."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids overhead
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('TEST_DB_URL')
    # Disable CSRF protection for testing
    WTF_CSRF_ENABLED: False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = environ.get('ADMINISTER_EMAIL')
    MAIL_PASSWORD = environ.get('APP_PASSWORD_EMAIL')
    DONT_REPLY_FROM_EMAIL =environ.get('ADMINISTER_EMAIL')
    ADMINS = (environ.get('ADMINISTER_EMAIL'),)
    MAIL_USE_TLS = True


class ProductionConfig(Config):
    pass


