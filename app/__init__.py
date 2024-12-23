from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from app.models import db

# Function to create and configure the Flask app
def create_app():
    app = Flask(__name__)
    
    # Load configuration from the 'config.py' file (silent=True prevents errors if the file is missing)
    app.config.from_pyfile('config.py', silent=True)

    # Initialize the database, migration, and JWT manager
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    # Register views blueprint for routing
    from app.views import views
    app.register_blueprint(views)

    # JWT error handling for expired token
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401

    # JWT error handling for invalid token
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Invalid token.", "error": "invalid_token"}), 401

    # JWT error handling for missing token
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message": "Missing access token.", "error": "authorization_required"}), 401

    return app
