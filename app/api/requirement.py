from flask import Blueprint, jsonify, request
from app.services.requirement_service import (
    create_requirement,
    get_requirement_by_id,
    get_all_requirements,
    update_requirement,
    delete_requirement,
    filter_all_requirements,
)
from app.utils.permisions import permission_required
from flask_jwt_extended import jwt_required

# Tạo một blueprint để định nghĩa API liên quan đến requirements
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

# Lọc yêu cầu
@requirements_bp.route("/requirements/filter", methods=["POST"])
@jwt_required()
@permission_required('requirement-index')
def filter_requirements():
    filters = request.get_json()
    requirements = filter_all_requirements(
        user_id=filters.get("user_id"),
        status=filters.get("status"),
        date=filters.get("date")
    )
    return jsonify(requirements), 200