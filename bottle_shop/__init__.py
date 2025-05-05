import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(test_config=None):
    """
    Create and configure the Flask application using the factory pattern.
    
    This factory function creates a new Flask application instance and configures:
    - Secret key for session security
    - Database connection to SQLite (default) or other DB via environment variable
    - Flask extensions (SQLAlchemy, Migrate, LoginManager)
    - Blueprints for modular route organization
    
    Args:
        test_config (dict, optional): Test configuration to override default settings
                                     Used primarily for testing. Defaults to None.
    
    Returns:
        Flask: A configured Flask application instance ready to run
    """
    app = Flask(__name__, instance_relative_config=True)
    
    # Set default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(app.instance_path, 'bottle_shop.sqlite')),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Set up user loader for Flask-Login
    from bottle_shop.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        # Updated to use newer SQLAlchemy style for Python 3.13 compatibility
        return db.session.execute(
            db.select(User).where(User.id == int(user_id))
        ).scalar_one_or_none()
    
    # Register blueprints
    from bottle_shop.controllers.main import main_bp
    app.register_blueprint(main_bp)
    
    from bottle_shop.controllers.takings import takings_bp
    app.register_blueprint(takings_bp, url_prefix='/takings')
    
    from bottle_shop.controllers.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app

# Import models to ensure they are registered with SQLAlchemy
from bottle_shop.models import daily_takings 