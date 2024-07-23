from flask import Flask
from flask_bootstrap import Bootstrap5
from app import models
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from app.utils.helpers import format_currency
from os import environ
from app.models import db

migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

def create_app(settings_module):
    
    app = Flask(__name__)
    app.config.from_object(settings_module)
        
    login_manager.init_app(app)  # Initialize Flask-Login
    login_manager.login_view = 'login'

    # User loader callback for Flask-Login (fetches user from database)
    @login_manager.user_loader
    def load_user(user_id):
        # Fetch user data from database or other source
        return models.User.query.get(user_id)

    # Create bootstrap from flask
    Bootstrap5(app)

    # Create ckeditor from flask
    CKEditor(app)


    # init database from models
    db.init_app(app)
    # Call db.create_all() here to ensure tables are created
    with app.app_context():
        db.create_all()
        
    # Import routes and register Blueprints
    from app.routes.user import user_bp
    from app.routes.api import api_bp
    from app.routes.project import project_bp
    from app.routes.index import index_bp
    from app.routes.profile import profile_bp
    from app.routes.api_documentation import api_doc_bp
    from app.routes.maps import maps_bp

    app.register_blueprint(profile_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(api_doc_bp)
    app.register_blueprint(maps_bp)

    # Add the format_currency function to the Jinja2 template context
    app.jinja_env.globals.update(format_currency=format_currency)
        
    return app