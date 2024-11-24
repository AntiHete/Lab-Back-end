from app import create_app
from app import database as db

from flask import jsonify, request
from datetime import datetime

app = create_app()  # Створення об'єкта Flask

# Заміна @app.get на @app.route з методами
@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    response = {
        "message": "Healthcheck is running",
        "date": datetime.today(),
        "status": "ok"
    }
    return jsonify(response), 200

# users
@app.route("/user", methods=["POST"])
def create_user():
    db.add_user(request.get_json())
    response = {
        "message": "User created",
        "date": datetime.today(),
        "status": "ok"
    }
    return jsonify(response), 201

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(db.get_all_users()), 200

@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = db.get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"message": "User not found"}), 404

@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if db.delete_user_by_id(user_id):
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"message": "User not found"}), 404

# categories
@app.route("/category", methods=["POST"])
def create_category():
    category = request.get_json()
    db.add_category(category)
    response = {
        "message": "Category created",
        "date": datetime.today(),
        "status": "ok"
    }
    return jsonify(response), 201

@app.route("/category", methods=["GET"])
def get_categories():
    return jsonify(db.get_all_categories()), 200

@app.route("/category/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    if db.delete_category(category_id):
        return jsonify({"message": "Category deleted"}), 200
    return jsonify({"message": "Category not found"}), 404

# records
@app.route("/record", methods=["POST"])
def create_record():
    record = request.get_json()
    db.add_record(record)
    response = {
        "message": "Record created",
        "date": datetime.today(),
        "status": "ok"
    }
    return jsonify(response), 201

@app.route("/record/<int:record_id>", methods=["GET"])
def get_record(record_id):
    record = db.get_record_by_id(record_id)
    if record:
        return jsonify(record), 200
    return jsonify({"message": "Record not found"}), 404

@app.route("/record/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    if db.delete_record(record_id):
        return jsonify({"message": "Record deleted"}), 200
    return jsonify({"message": "Record not found"}), 404

@app.route("/record", methods=["GET"])
def get_records():
    user_id = request.args.get("user_id", type=int)
    category_id = request.args.get("category_id", type=int)

    if user_id is None and category_id is None:
        return jsonify({"message": "user_id or category_id is required"}), 400
    records = db.get_records_by_user_and_category(user_id, category_id)
    return jsonify(records), 200
