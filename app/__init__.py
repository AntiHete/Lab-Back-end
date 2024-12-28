from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from app.models import db


def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)

    # Load configuration from the 'config.py' file
    app.config.from_pyfile('config.py', silent=True)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    # Register blueprints
    from app.views import views
    app.register_blueprint(views)

    # Configure JWT error handling
    configure_jwt_errors(app)

    return app

def configure_jwt_errors(app):
    """
    Configure JWT error handlers for the application.
    """
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401


    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Invalid token.", "error": "invalid_token"}), 401


    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message": "Missing access token.", "error": "authorization_required"}), 401

    return app
