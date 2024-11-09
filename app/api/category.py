from flask import Blueprint, jsonify, request
from app.services.category_service import (
    create_category,
    get_category_by_id,
    filter_all_categories,
    update_category,
    delete_category,
    get_all_categories
   
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
# @categories_bp.route("/categories", methods=["GET"])
# @jwt_required()
# @permission_required('category-index')
# def read_categories():
#     categories = get_all_categories()
#     return jsonify(categories), 200

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

# Lấy tất cả danh mục hoặc phân trang và lọc
@categories_bp.route("/categories", methods=["GET"])
@jwt_required()
@permission_required('category-index')
def manage_categories():
    # Lấy các tham số từ query để áp dụng bộ lọc và phân trang
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    min_lifespan = request.args.get('min_lifespan', type=int, default=None)
    max_lifespan = request.args.get('max_lifespan', type=int, default=None)
    name = request.args.get('name', type=str, default=None)
    default_salvage_value_rate = request.args.get('default_salvage_value_rate', type=float, default=None)
    parent_id = request.args.get('parent_id', type=int, default=None)

    # Gọi hàm filter_all_categories với các tham số
    result = filter_all_categories(
        page=page, 
        per_page=per_page, 
        min_lifespan=min_lifespan, 
        max_lifespan=max_lifespan,
        name=name,
        default_salvage_value_rate=default_salvage_value_rate,
        parent_id=parent_id
    )

    return jsonify(result), 200
