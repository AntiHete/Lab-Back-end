from flask import Blueprint, request
from app.models import db, CategoryModel
from app.schemas import CategorySchema

bp = Blueprint("categories", __name__, url_prefix="/categories")

@bp.route("/", methods=["POST"])
def create_category():
    data = request.json
    schema = CategorySchema()
    validated_data = schema.load(data)
    category = CategoryModel(**validated_data)
    db.session.add(category)
    db.session.commit()
    return schema.dump(category), 201

@bp.route("/", methods=["GET"])
def list_categories():
    categories = CategoryModel.query.all()
    schema = CategorySchema(many=True)
    return schema.dump(categories), 200
