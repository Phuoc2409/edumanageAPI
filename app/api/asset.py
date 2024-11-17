from flask import Blueprint, jsonify, request
from app.services.asset_service import (
    create_asset,
    get_asset_by_id,
    get_all_assets,
    update_asset,
    delete_asset,
    get_floors_by_building
)
from app.utils.permisions import permission_required
from flask_jwt_extended import jwt_required

# Tạo một blueprint để định nghĩa API liên quan đến assets
assets_bp = Blueprint("assets", __name__)

# Tạo tài sản mới
@assets_bp.route("/assets", methods=["POST"])
@jwt_required()
@permission_required('asset-add')
def add_asset():
    asset_data = request.get_json()
    asset = create_asset(asset_data)
    return jsonify(asset), 201

# Lấy tất cả tài sản
@assets_bp.route("/assets", methods=["GET"])
@jwt_required()
@permission_required('asset-index')
def read_assets():
    assets = get_all_assets()
    return jsonify(assets), 200

# Lấy tài sản theo ID
@assets_bp.route("/assets/<int:asset_id>", methods=["GET"])
@jwt_required()
@permission_required('asset-index')
def read_asset(asset_id):
    asset = get_asset_by_id(asset_id)
    if asset is None:
        return jsonify({"error": "Asset not found"}), 404
    return jsonify(asset), 200

# Cập nhật tài sản
@assets_bp.route("/assets/<int:asset_id>", methods=["PUT"])
@jwt_required()
@permission_required('asset-edit')
def update_asset_api(asset_id):
    asset_data = request.get_json()
    updated_asset = update_asset(asset_id, asset_data)
    if updated_asset is None:
        return jsonify({"error": "Asset not found"}), 404
    return jsonify(updated_asset), 200

# Xóa tài sản
@assets_bp.route("/assets/<int:asset_id>", methods=["DELETE"])
@jwt_required()
@permission_required('asset-delete')
def delete_asset_api(asset_id):
    if delete_asset(asset_id):
        return jsonify({"message": "Asset deleted successfully"}), 204
    return jsonify({"error": "Asset not found"}), 404

@assets_bp.route("/floors/<int:building_id>", methods=["GET"])
def get_floors(building_id):
    floors = get_floors_by_building(building_id)
    if not floors:
        return jsonify({"error": "Building not found"}), 404
    return jsonify(floors), 200