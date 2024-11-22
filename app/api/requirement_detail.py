from flask import Blueprint, jsonify, request
from app.services.requirement_detail_service import (
    create_requirement_detail,
    get_requirement_detail_by_id,
    get_all_requirement_details,
    update_requirement_detail,
    delete_requirement_detail,
    get_specific_requirement_detail,
)
from app.utils.permisions import permission_required
from flask_jwt_extended import jwt_required

# Tạo một blueprint để định nghĩa API liên quan đến requirement details
requirement_details_bp = Blueprint("requirement_details", __name__)

# Tạo chi tiết yêu cầu mới
@requirement_details_bp.route("/requirement-details", methods=["POST"])
@jwt_required()
@permission_required('requirement-detail-add')
def add_requirement_detail():
    requirement_detail_data = request.get_json()
    requirement_detail = create_requirement_detail(requirement_detail_data)
    return jsonify(requirement_detail), 201

# Lấy tất cả chi tiết yêu cầu
@requirement_details_bp.route("/requirement-details", methods=["GET"])
@jwt_required()
#@permission_required('requirement-detail-index')
def read_requirement_details():
    requirement_details = get_all_requirement_details()
    return jsonify(requirement_details), 200

# Lấy chi tiết yêu cầu theo ID
@requirement_details_bp.route("/requirement-details/<int:requirement_detail_id>", methods=["GET"])
@jwt_required()
@permission_required('requirement-detail-index')
def read_requirement_detail(requirement_detail_id):
    requirement_detail = get_requirement_detail_by_id(requirement_detail_id)
    if requirement_detail is None:
        return jsonify({"error": "Requirement detail not found"}), 404
    return jsonify(requirement_detail), 200

# Cập nhật chi tiết yêu cầu
@requirement_details_bp.route("/requirement-details/<int:requirement_detail_id>", methods=["PUT"])
@jwt_required()
@permission_required('requirement-detail-edit')
def update_requirement_detail_api(requirement_detail_id):
    requirement_detail_data = request.get_json()
    updated_requirement_detail = update_requirement_detail(requirement_detail_id, requirement_detail_data)
    if updated_requirement_detail is None:
        return jsonify({"error": "Requirement detail not found"}), 404
    return jsonify(updated_requirement_detail), 200

# Xóa chi tiết yêu cầu
@requirement_details_bp.route("/requirement-details/<int:requirement_detail_id>", methods=["DELETE"])
@jwt_required()
@permission_required('requirement-detail-delete')
def delete_requirement_detail_api(requirement_detail_id):
    if delete_requirement_detail(requirement_detail_id):
        return jsonify({"message": "Requirement detail deleted successfully"}), 204
    return jsonify({"error": "Requirement detail not found"}), 404


requirement_details_bp.route("/requirement-details/specific-requirement-details/<int:requirement_id>", methods=["GET"])
@jwt_required()
#@permission_required('requirement-detail-index')
def get_requirement_with_type_api(requirement_id):
    requirement_data = get_specific_requirement_detail(requirement_id)
    if not requirement_data:
        return jsonify({"error": "Requirement not found"}), 404
    return jsonify(requirement_data), 200