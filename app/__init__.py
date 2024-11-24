from app import views
from flask import Flask
from app.extensions import db, migrate
from app.models import UserModel, CategoryModel, ExpenseModel
from app.routes.categories import bp as categories_bp

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate.init_app(app, db)

 # Register Blueprints
    app.register_blueprint(categories_bp)

    return app
