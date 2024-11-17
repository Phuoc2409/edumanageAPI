from flask import Blueprint, jsonify, request
from app.services.asset_detail_service import (
    create_asset_detail,
    get_asset_detail_by_id,
    get_all_asset_details,
    update_asset_detail,
    delete_asset_detail,
    get_rooms_by_floor,
    filter_asset_details,
    filter_asset_details_by_room_floor_building
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

@asset_details_bp.route('/asset-details/filter-by-building-floor-room', methods=['POST'])
def filter_by_floor_and_room_api():
    try:
        # Lấy dữ liệu từ body request
        filters = request.get_json()

        # Gọi service lọc theo ID tầng và phòng
        filtered_results = filter_asset_details_by_room_floor_building(filters)

        # Trả về kết quả
        return jsonify(filtered_results), 200
    except Exception as e:
        return jsonify({"error": f"Error filtering asset details: {str(e)}"}), 500
    
#Lọc chi tiết tài sản
@asset_details_bp.route('/asset-details/filter', methods=['POST'])
def get_filter_asset_details():
    try:
        # Lấy dữ liệu từ request body
        filters = request.get_json()

        # Gọi service với dữ liệu body
        filtered_results = filter_asset_details(filters)

        # Trả về kết quả
        return jsonify(filtered_results), 200
    except Exception as e:
        return jsonify({"error": f"Error filtering asset details: {str(e)}"}), 500
    

@asset_details_bp.route('/rooms/<int:floor_id>', methods=['GET'])
def rooms(floor_id):
    return jsonify(get_rooms_by_floor(floor_id))