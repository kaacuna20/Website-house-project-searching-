from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from housing_finder_app import models
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
import locale


load_dotenv(".env")
db = models.db
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

def create_app(settings_module=os.getenv("CONFIGURATION_SETUP")):
    app = Flask(__name__, instance_relative_config=True)  # Allows instance configuration
    #app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config.from_object(settings_module)
    app.config.from_pyfile('config.py', silent=True)

    login_manager.init_app(app)  # Initialize Flask-Login
    login_manager.login_view = 'login'

    # User loader callback for Flask-Login (fetches user from database)
    @login_manager.user_loader
    def load_user(user_id):
        # Fetch user data from database or other source
        return models.User.query.get(user_id)


    # Create bootstrap from flask
    bootstrap = Bootstrap5(app)

    # Create ckeditor from flask
    ckeditor = CKEditor(app)

    # init database from models
    db.init_app(app)

    # Call db.create_all() here to ensure tables are created
    with app.app_context():
        db.create_all()

    migrate.init_app(app, db)
    # initialite mail in app
    mail.init_app(app)

    # Import routes and register Blueprints
    from housing_finder_app.routes.user import user_bp
    from housing_finder_app.routes.api import api_bp
    from housing_finder_app.routes.project import project_bp
    from housing_finder_app.routes.index import index_bp
    from housing_finder_app.routes.profile import profile_bp
    from housing_finder_app.routes.api_documentation import api_doc_bp

    app.register_blueprint(profile_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(project_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(api_doc_bp)

    @app.template_filter()
    def format_currency(value):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # Set locale to use proper currency formatting
        return locale.currency(value, grouping=True)

    return app