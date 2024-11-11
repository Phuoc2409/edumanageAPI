from flask import Blueprint, jsonify, request
from app.services.asset_detail_service import (
    create_asset_detail,
    get_asset_detail_by_id,
    get_all_asset_details,
    update_asset_detail,
    delete_asset_detail,
)
from app.utils.permisions import permission_required
from flask_jwt_extended import jwt_required

# Tạo một blueprint để định nghĩa API liên quan đến asset details
asset_details_bp = Blueprint("asset_details", __name__)

# Tạo chi tiết tài sản mới
@asset_details_bp.route("/asset-details", methods=["POST"])
@jwt_required()
@permission_required('asset-details-add')
def add_asset_detail():
    asset_detail_data = request.get_json()
    asset_detail = create_asset_detail(asset_detail_data)
    return jsonify(asset_detail), 201

# Lấy tất cả chi tiết tài sản
@asset_details_bp.route("/asset-details", methods=["GET"])
@jwt_required()
@permission_required('asset-details-index')
def read_asset_details():
    asset_details = get_all_asset_details()
    return jsonify(asset_details), 200

# Lấy chi tiết tài sản theo ID
@asset_details_bp.route("/asset-details/<int:asset_detail_id>", methods=["GET"])
@jwt_required()
@permission_required('asset-details-index')
def read_asset_detail(asset_detail_id):
    asset_detail = get_asset_detail_by_id(asset_detail_id)
    if asset_detail is None:
        return jsonify({"error": "Asset detail not found"}), 404
    return jsonify(asset_detail), 200

# Cập nhật chi tiết tài sản
@asset_details_bp.route("/asset-details/<int:asset_detail_id>", methods=["PUT"])
@jwt_required()
@permission_required('asset-details-edit')
def update_asset_detail_api(asset_detail_id):
    asset_detail_data = request.get_json()
    updated_asset_detail = update_asset_detail(asset_detail_id, asset_detail_data)
    if updated_asset_detail is None:
        return jsonify({"error": "Asset detail not found"}), 404
    return jsonify(updated_asset_detail), 200

# Xóa chi tiết tài sản
@asset_details_bp.route("/asset-details/<int:asset_detail_id>", methods=["DELETE"])
@jwt_required()
@permission_required('asset-details-delete')
def delete_asset_detail_api(asset_detail_id):
    if delete_asset_detail(asset_detail_id):
        return jsonify({"message": "Asset detail deleted successfully"}), 204
    return jsonify({"error": "Asset detail not found"}), 404


#Lọc chi tiết tài sản
from app.services.asset_detail_service import search_asset_details
@asset_details_bp.route("/asset_details/search", methods=["GET"])
@jwt_required()
@permission_required('asset-details-index')
def search_asset_details_route():
    # Lấy các tham số tìm kiếm từ request
    filters = {
        "identifier_number": request.args.get("identifier_number"),
        "user_id": request.args.get("user_id"),
        "start_date": request.args.get("start_date"),  # Ngày bắt đầu
        "end_date": request.args.get("end_date"),      # Ngày kết thúc
        "min_price": request.args.get("min_price"),    # Giá tối thiểu
        "max_price": request.args.get("max_price"),    # Giá tối đa
        "status": request.args.get("status"),
        "category_id": request.args.get("category_id"),
        "asset_id": request.args.get("asset_id"),
    }
    
    # Loại bỏ các tham số không có giá trị
    filters = {key: value for key, value in filters.items() if value is not None}

    # Thực hiện tìm kiếm
    asset_details = search_asset_details(filters)
    
    return jsonify(asset_details), 200