from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    default_currency = db.Column(db.String(3), nullable=False, default="USD")
    categories = db.relationship("CategoryModel", back_populates="user", lazy="dynamic")
    expenses = db.relationship("ExpenseModel", back_populates="user", lazy="dynamic")


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    is_global = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    user = db.relationship("UserModel", back_populates="categories")


class ExpenseModel(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    user = db.relationship("UserModel", back_populates="expenses")
    category = db.relationship("CategoryModel", back_populates="categories")
