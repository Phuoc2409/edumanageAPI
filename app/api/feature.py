from flask import Blueprint, jsonify, request
from app.services.feature_service import (
    create_feature,
    get_feature_by_id,
    get_all_features,
    update_feature,
    delete_feature,
)
from app.utils.permisions import permission_required
from flask_jwt_extended import jwt_required

# Tạo một blueprint để định nghĩa API liên quan đến features
features_bp = Blueprint("features", __name__)

# Tạo tính năng mới
@features_bp.route("/features", methods=["POST"])
@jwt_required()
@permission_required('feature-add')
def add_feature():
    feature_data = request.get_json()
    feature = create_feature(feature_data)
    return jsonify(feature), 201

# Lấy tất cả tính năng
@features_bp.route("/features", methods=["GET"])
@jwt_required()
@permission_required('feature-index')
def read_features():
    features = get_all_features()
    return jsonify(features), 200

# Lấy tính năng theo ID
@features_bp.route("/features/<int:feature_id>", methods=["GET"])
@jwt_required()
@permission_required('feature-index')
def read_feature(feature_id):
    feature = get_feature_by_id(feature_id)
    if feature is None:
        return jsonify({"error": "Feature not found"}), 404
    return jsonify(feature), 200

# Cập nhật tính năng
@features_bp.route("/features/<int:feature_id>", methods=["PUT"])
@jwt_required()
@permission_required('feature-edit')
def update_feature_api(feature_id):
    feature_data = request.get_json()
    updated_feature = update_feature(feature_id, feature_data)
    if updated_feature is None:
        return jsonify({"error": "Feature not found"}), 404
    return jsonify(updated_feature), 200

# Xóa tính năng
@features_bp.route("/features/<int:feature_id>", methods=["DELETE"])
@jwt_required()
@permission_required('feature-delete')
def delete_feature_api(feature_id):
    if delete_feature(feature_id):
        return jsonify({"message": "Feature deleted successfully"}), 204
    return jsonify({"error": "Feature not found"}), 404
