from flask_sqlalchemy import SQLAlchemy

# Initialize the database instance
db = SQLAlchemy()

# Model for transactions
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, description="Unique identifier for the transaction")
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False, description="Associated account ID")
    amount = db.Column(db.Float, nullable=False, description="Transaction amount")
    timestamp = db.Column(db.DateTime, nullable=False, description="Transaction timestamp")

# Model for user accounts
class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, description="Unique identifier for the account")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, description="ID of the user associated with the account")
    balance = db.Column(db.Float, default=0.0, nullable=False, description="Account balance")
    transactions = db.relationship('Transaction', backref='account', lazy=True)

# Model for user information
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, description="Unique identifier for the user")
    username = db.Column(db.String(80), unique=True, nullable=False, description="Unique username")
    email = db.Column(db.String(120), unique=True, nullable=False, description="User email address")
    password = db.Column(db.String(128), nullable=False, description="Securely hashed password")
    accounts = db.relationship('Accounts', backref='user', lazy=True)
