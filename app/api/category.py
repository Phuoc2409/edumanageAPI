from flask import Blueprint, jsonify, request
from datetime import datetime
from app.services.category_service import (
    create_category,
    get_category_by_id,
    filter_all_categories,
    update_category,
    delete_category,
    get_all_categories,
    get_all_buildings,
    get_category_statistics,
    get_purchase_statistics
   
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

@categories_bp.route("/categories/filter", methods=["POST"])
@jwt_required()
@permission_required('category-index')
def filter_categories():
    filters = request.get_json()
    categories = filter_all_categories(
        min_lifespan=filters.get("min_lifespan"),
        max_lifespan=filters.get("max_lifespan"),
        name=filters.get("name"),
        description=filters.get("description"),
        default_salvage_value_rate=filters.get("default_salvage_value_rate"),
        parent_id=filters.get("parent_id"),
        
    )
    return jsonify(categories), 200

@categories_bp.route("/buildings", methods=["GET"])
def get_buildings():
    buildings = get_all_buildings()
    return jsonify({"buildings": buildings})

# Thống kê tài sản
@categories_bp.route('/categories/statistics', methods=['GET'])
@jwt_required()
@permission_required('category-index')
def category_statistics_api():

    result = get_category_statistics()
    return jsonify(result), 200

@categories_bp.route('/categories/purchase_statistics', methods=['POST'])
@jwt_required()
@permission_required('category-index')
def category_purchase_statistics_api():
    """
    API lấy thống kê số sản phẩm đã mua và tổng tiền đã chi theo danh mục trong khoảng thời gian (dùng POST).
    """
    # Lấy khoảng thời gian từ body của POST request
    data = request.get_json()

    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')

    if not start_date_str or not end_date_str:
        return jsonify({"error": "start_date and end_date are required."}), 400

    # Chuyển đổi ngày từ chuỗi sang đối tượng datetime
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Lấy thống kê
    result = get_purchase_statistics(start_date, end_date)
    return jsonify(result), 200