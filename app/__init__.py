from app import views
from flask import Flask
from app.extensions import db, migrate
from app.models import UserModel, CategoryModel, ExpenseModel

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate.init_app(app, db)
    return app
