from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Database instance
from app.models import db

# Migrate instance
migrate = Migrate()

def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)
    
    # Load configuration from 'config.py'
    app.config.from_pyfile('config.py', silent=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    return app
