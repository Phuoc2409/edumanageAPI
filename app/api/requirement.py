from flask import Blueprint, request, jsonify
from ..services.requirement_service import (
    create_requirement,
    get_all_requirements,
    get_requirement_by_id,
    update_requirement,
    delete_requirement
)

requirements_bp = Blueprint('requirements_bp', __name__)

# Route để lấy danh sách tất cả yêu cầu
@requirements_bp.route('/requirements', methods=['GET'])
def list_requirements():
    requirements = get_all_requirements()
    return jsonify(requirements), 200


# Route để lấy thông tin chi tiết yêu cầu
@requirements_bp.route('/requirements/<int:requirement_id>', methods=['GET'])
def get_requirement(requirement_id):
    requirement = get_requirement_by_id(requirement_id)
    if not requirement:
        return jsonify({"message": "Requirement not found"}), 404
    return jsonify(requirement), 200


# Route để tạo mới yêu cầu
@requirements_bp.route('/requirements', methods=['POST'])
def create_new_requirement():
    data = request.json
    required_fields = ["user_id", "date", "description", "status"]
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    new_requirement = create_requirement(data)
    return jsonify(new_requirement), 201


# Route để cập nhật yêu cầu
@requirements_bp.route('/requirements/<int:requirement_id>', methods=['PUT'])
def update_existing_requirement(requirement_id):
    data = request.json
    updated_requirement = update_requirement(requirement_id, data)
    if not updated_requirement:
        return jsonify({"message": "Requirement not found"}), 404
    return jsonify(updated_requirement), 200


# Route để xóa yêu cầu
@requirements_bp.route('/requirements/<int:requirement_id>', methods=['DELETE'])
def delete_existing_requirement(requirement_id):
    success = delete_requirement(requirement_id)
    if not success:
        return jsonify({"message": "Requirement not found"}), 404
    return jsonify({"message": "Requirement deleted successfully"}), 200
