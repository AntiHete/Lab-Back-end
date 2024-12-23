from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Model for user accounts
class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, description="Unique identifier for the account")
    user_id = db.Column(db.Integer, nullable=False, unique=True, description="ID of the user associated with the account")
    balance = db.Column(db.Float, default=0.0, nullable=False, description="Account balance (must be non-negative)")

# Model for user information
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, description="Unique identifier for the user")
    username = db.Column(db.String(80), unique=True, nullable=False, description="Username (must be unique)")
    password = db.Column(db.String(128), nullable=False, description="Password (must be securely hashed)")
