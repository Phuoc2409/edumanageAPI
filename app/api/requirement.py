from flask import Blueprint, jsonify, request
from app.services.requirement_service import (
    create_requirement,
    get_requirement_by_id,
    get_all_requirements,
    update_requirement,
    delete_requirement,
)
from app.utils.permisions import permission_required
from flask_jwt_extended import jwt_required

# Tạo một blueprint để định nghĩa API liên quan đến requirements
requirements_bp = Blueprint("requirements", __name__)

# Tạo yêu cầu mới
@requirements_bp.route("/requirements", methods=["POST"])
@jwt_required()
@permission_required('requirement-add')
def add_requirement():
    requirement_data = request.get_json()
    requirement = create_requirement(requirement_data)
    return jsonify(requirement), 201

# Lấy tất cả yêu cầu
@requirements_bp.route("/requirements", methods=["GET"])
@jwt_required()
@permission_required('requirement-index')
def read_requirements():
    requirements = get_all_requirements()
    return jsonify(requirements), 200

# Lấy yêu cầu theo ID
@requirements_bp.route("/requirements/<int:requirement_id>", methods=["GET"])
@jwt_required()
@permission_required('requirement-index')
def read_requirement(requirement_id):
    requirement = get_requirement_by_id(requirement_id)
    if requirement is None:
        return jsonify({"error": "Requirement not found"}), 404
    return jsonify(requirement), 200

# Cập nhật yêu cầu
@requirements_bp.route("/requirements/<int:requirement_id>", methods=["PUT"])
@jwt_required()
@permission_required('requirement-edit')
def update_requirement_api(requirement_id):
    requirement_data = request.get_json()
    updated_requirement = update_requirement(requirement_id, requirement_data)
    if updated_requirement is None:
        return jsonify({"error": "Requirement not found"}), 404
    return jsonify(updated_requirement), 200

# Xóa yêu cầu
@requirements_bp.route("/requirements/<int:requirement_id>", methods=["DELETE"])
@jwt_required()
@permission_required('requirement-delete')
def delete_requirement_api(requirement_id):
    if delete_requirement(requirement_id):
        return jsonify({"message": "Requirement deleted successfully"}), 204
    return jsonify({"error": "Requirement not found"}), 404
