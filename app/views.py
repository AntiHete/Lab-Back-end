from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text

from app import mock_database as db_helper
from app.models import db, User, Account, Transaction, Category
from app.schemas import UserSchema, AccountSchema, TransactionSchema, CategorySchema

api = Blueprint("api", __name__)

user_schema = UserSchema()
account_schema = AccountSchema()
transaction_schema = TransactionSchema()
category_schema = CategorySchema()

# Healthcheck
@api.route("/status", methods=["GET"])
def status():
    return jsonify({
        "status": "running",
        "timestamp": datetime.now()
    }), 200

# User management
@api.route("/users/register", methods=["POST"])
def register():
    payload = request.get_json()
    errors = user_schema.validate(payload)
    if errors:
        return jsonify(errors), 400

    new_user = User(
        username=payload["username"],
        password=pbkdf2_sha256.hash(payload["password"])
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username already taken"}), 400

    return jsonify({"message": "User created", "user_id": new_user.id}), 201

@api.route("/users/login", methods=["POST"])
def login():
    payload = request.get_json()
    errors = user_schema.validate(payload)
    if errors:
        return jsonify(errors), 400

    user = User.query.filter_by(username=payload["username"]).first()
    if user and pbkdf2_sha256.verify(payload["password"], user.password):
        token = create_access_token(identity=user.id)
        return jsonify({"token": token, "user_id": user.id}), 200

    return jsonify({"error": "Invalid credentials"}), 401

@api.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    current_user = get_jwt_identity()
    if int(current_user) != user_id:
        return jsonify({"error": "Unauthorized access"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user_schema.dump(user)), 200

# Account management
@api.route("/accounts", methods=["POST"])
@jwt_required()
def create_account():
    payload = request.get_json()
    errors = account_schema.validate(payload)
    if errors:
        return jsonify(errors), 400

    current_user = get_jwt_identity()
    if int(current_user) != payload["user_id"]:
        return jsonify({"error": "Unauthorized access"}), 403

    account = Account(user_id=payload["user_id"], balance=payload.get("balance", 0))

    try:
        db.session.add(account)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Account already exists"}), 400

    return jsonify(account_schema.dump(account)), 201

@api.route("/accounts/<int:user_id>", methods=["GET"])
@jwt_required()
def get_account(user_id):
    current_user = get_jwt_identity()
    if int(current_user) != user_id:
        return jsonify({"error": "Unauthorized access"}), 403

    account = Account.query.filter_by(user_id=user_id).first()
    if not account:
        return jsonify({"error": "Account not found"}), 404

    return jsonify(account_schema.dump(account)), 200

@api.route("/accounts/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_account(user_id):
    current_user = get_jwt_identity()
    if int(current_user) != user_id:
        return jsonify({"error": "Unauthorized access"}), 403

    account = Account.query.filter_by(user_id=user_id).first()
    if not account:
        return jsonify({"error": "Account not found"}), 404

    db.session.delete(account)
    db.session.commit()
    return jsonify({"message": "Account deleted"}), 200

# Transactions
@api.route("/transactions", methods=["POST"])
@jwt_required()
def create_transaction():
    payload = request.get_json()
    errors = transaction_schema.validate(payload)
    if errors:
        return jsonify(errors), 400

    current_user = get_jwt_identity()
    if int(current_user) != payload["user_id"]:
        return jsonify({"error": "Unauthorized access"}), 403

    account = Account.query.filter_by(user_id=payload["user_id"]).first()
    if not account:
        return jsonify({"error": "Account not found"}), 404

    if payload["type"] == "withdrawal" and account.balance < payload["amount"]:
        return jsonify({"error": "Insufficient funds"}), 400

    account.balance += payload["amount"] if payload["type"] == "deposit" else -payload["amount"]
    db.session.commit()

    new_transaction = Transaction(
        user_id=payload["user_id"],
        type=payload["type"],
        amount=payload["amount"],
        timestamp=datetime.now()
    )
    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({"message": "Transaction successful", "new_balance": account.balance}), 201

@api.route("/transactions/history", methods=["GET"])
@jwt_required()
def transaction_history():
    current_user = get_jwt_identity()
    transactions = Transaction.query.filter_by(user_id=current_user).all()
    return jsonify(transaction_schema.dump(transactions, many=True)), 200

# Categories
@api.route("/categories", methods=["POST"])
@jwt_required()
def create_category():
    payload = request.get_json()
    errors = category_schema.validate(payload)
    if errors:
        return jsonify(errors), 400

    new_category = Category(name=payload["name"], description=payload.get("description"))
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"message": "Category created", "category_id": new_category.id}), 201

@api.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify(category_schema.dump(categories, many=True)), 200

@api.route("/categories/<int:category_id>", methods=["DELETE"])
@jwt_required()
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 200

# Data Export
@api.route("/export/transactions", methods=["GET"])
@jwt_required()
def export_transactions():
    current_user = get_jwt_identity()
    transactions = Transaction.query.filter_by(user_id=current_user).all()
    if not transactions:
        return jsonify({"error": "No transactions to export"}), 404

    export_data = [
        {
            "type": t.type,
            "amount": t.amount,
            "timestamp": t.timestamp
        } for t in transactions
    ]

    return jsonify({"exported_data": export_data}), 200
