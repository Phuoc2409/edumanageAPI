from flask import Blueprint, jsonify, request
from app.services.category_service import (
    create_category,
    get_category_by_id,
    get_all_categories,
    update_category,
    delete_category,
)
from app.utils.permisions import permission_required
from flask_jwt_extended import jwt_required

# Tạo một blueprint để định nghĩa API liên quan đến categories
categories_bp = Blueprint("categories", __name__)

# Tạo danh mục mới
@categories_bp.route("/categories", methods=["POST"])
@jwt_required()
@permission_required('category-add')
def add_category():
    category_data = request.get_json()
    category = create_category(category_data)
    return jsonify(category), 201

# Lấy tất cả danh mục
@categories_bp.route("/categories", methods=["GET"])
@jwt_required()
@permission_required('category-index')
def read_categories():
    categories = get_all_categories()
    return jsonify(categories), 200

# Lấy danh mục theo ID
@categories_bp.route("/categories/<int:category_id>", methods=["GET"])
@jwt_required()
@permission_required('category-index')
def read_category(category_id):
    category = get_category_by_id(category_id)
    if category is None:
        return jsonify({"error": "Category not found"}), 404
    return jsonify(category), 200

# Cập nhật danh mục
@categories_bp.route("/categories/<int:category_id>", methods=["PUT"])
@jwt_required()
@permission_required('category-edit')
def update_category_api(category_id):
    category_data = request.get_json()
    updated_category = update_category(category_id, category_data)
    if updated_category is None:
        return jsonify({"error": "Category not found"}), 404
    return jsonify(updated_category), 200

# Xóa danh mục
@categories_bp.route("/categories/<int:category_id>", methods=["DELETE"])
@jwt_required()
@permission_required('category-delete')
def delete_category_api(category_id):
    if delete_category(category_id):
        return jsonify({"message": "Category deleted successfully"}), 204
    return jsonify({"error": "Category not found"}), 404
