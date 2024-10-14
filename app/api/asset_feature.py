from flask import Blueprint, jsonify, request
from app.services.asset_feature_service import (
    create_asset_feature,
    get_asset_feature_by_id,
    get_all_asset_features,
    update_asset_feature,
    delete_asset_feature,
)
from app.utils.permisions import permission_required
from flask_jwt_extended import jwt_required

# Tạo một blueprint để định nghĩa API liên quan đến asset features
asset_features_bp = Blueprint("asset_features", __name__)

# Tạo tính năng tài sản mới
@asset_features_bp.route("/asset-features", methods=["POST"])
@jwt_required()
@permission_required('asset-feature-add')
def add_asset_feature():
    asset_feature_data = request.get_json()
    asset_feature = create_asset_feature(asset_feature_data)
    return jsonify(asset_feature), 201

# Lấy tất cả tính năng tài sản
@asset_features_bp.route("/asset-features", methods=["GET"])
@jwt_required()
@permission_required('asset-feature-index')
def read_asset_features():
    asset_features = get_all_asset_features()
    return jsonify(asset_features), 200

# Lấy tính năng tài sản theo ID
@asset_features_bp.route("/asset-features/<int:asset_feature_id>", methods=["GET"])
@jwt_required()
@permission_required('asset-feature-index')
def read_asset_feature(asset_feature_id):
    asset_feature = get_asset_feature_by_id(asset_feature_id)
    if asset_feature is None:
        return jsonify({"error": "Asset feature not found"}), 404
    return jsonify(asset_feature), 200

# Cập nhật tính năng tài sản
@asset_features_bp.route("/asset-features/<int:asset_feature_id>", methods=["PUT"])
@jwt_required()
@permission_required('asset-feature-edit')
def update_asset_feature_api(asset_feature_id):
    asset_feature_data = request.get_json()
    updated_asset_feature = update_asset_feature(asset_feature_id, asset_feature_data)
    if updated_asset_feature is None:
        return jsonify({"error": "Asset feature not found"}), 404
    return jsonify(updated_asset_feature), 200

# Xóa tính năng tài sản
@asset_features_bp.route("/asset-features/<int:asset_feature_id>", methods=["DELETE"])
@jwt_required()
@permission_required('asset-feature-delete')
def delete_asset_feature_api(asset_feature_id):
    if delete_asset_feature(asset_feature_id):
        return jsonify({"message": "Asset feature deleted successfully"}), 204
    return jsonify({"error": "Asset feature not found"}), 404
