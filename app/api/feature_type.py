from flask import Blueprint, jsonify, request
from app.services.feature_type_service import (
    create_feature_type,
    get_feature_type_by_id,
    get_all_feature_types,
    update_feature_type,
    delete_feature_type,
)
from app.utils.permisions import permission_required
from flask_jwt_extended import jwt_required

# Tạo một blueprint để định nghĩa API liên quan đến feature types
feature_types_bp = Blueprint("feature_types", __name__)

# Tạo loại tính năng mới
@feature_types_bp.route("/feature-types", methods=["POST"])
@jwt_required()
@permission_required('feature-type-add')
def add_feature_type():
    feature_type_data = request.get_json()
    feature_type = create_feature_type(feature_type_data)
    return jsonify(feature_type), 201

# Lấy tất cả loại tính năng
@feature_types_bp.route("/feature-types", methods=["GET"])
@jwt_required()
@permission_required('feature-type-index')
def read_feature_types():
    feature_types = get_all_feature_types()
    return jsonify(feature_types), 200

# Lấy loại tính năng theo ID
@feature_types_bp.route("/feature-types/<int:feature_type_id>", methods=["GET"])
@jwt_required()
@permission_required('feature-type-index')
def read_feature_type(feature_type_id):
    feature_type = get_feature_type_by_id(feature_type_id)
    if feature_type is None:
        return jsonify({"error": "Feature type not found"}), 404
    return jsonify(feature_type), 200

# Cập nhật loại tính năng
@feature_types_bp.route("/feature-types/<int:feature_type_id>", methods=["PUT"])
@jwt_required()
@permission_required('feature-type-edit')
def update_feature_type_api(feature_type_id):
    feature_type_data = request.get_json()
    updated_feature_type = update_feature_type(feature_type_id, feature_type_data)
    if updated_feature_type is None:
        return jsonify({"error": "Feature type not found"}), 404
    return jsonify(updated_feature_type), 200

# Xóa loại tính năng
@feature_types_bp.route("/feature-types/<int:feature_type_id>", methods=["DELETE"])
@jwt_required()
@permission_required('feature-type-delete')
def delete_feature_type_api(feature_type_id):
    if delete_feature_type(feature_type_id):
        return jsonify({"message": "Feature type deleted successfully"}), 204
    return jsonify({"error": "Feature type not found"}), 404
