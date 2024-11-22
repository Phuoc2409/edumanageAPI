from flask import Blueprint, request, jsonify
from app.services.role_service import (
    create_role,
    get_all_roles,
    get_role_by_id,
    update_role,
    delete_role
)
role_bp = Blueprint('role_bp', __name__)
# Route để lấy danh sách tất cả vai trò
@role_bp.route('/roles', methods=['GET'])
def list_roles():
    roles = get_all_roles()
    return jsonify(roles), 200
# Route để lấy thông tin chi tiết vai trò
@role_bp.route('/roles/<int:role_id>', methods=['GET'])
def get_role(role_id):
    role = get_role_by_id(role_id)
    if not role:
        return jsonify({"message": "Role not found"}), 404
    return jsonify(role), 200
# Route để tạo mới vai trò
@role_bp.route('/roles', methods=['POST'])
def create_new_role():
    data = request.json
    if not data or "role_name" not in data or "description" not in data:
        return jsonify({"message": "Missing required fields"}), 400
    new_role = create_role(data)
    return jsonify(new_role), 201
# Route để cập nhật vai trò
@role_bp.route('/roles/<int:role_id>', methods=['PUT'])
def update_existing_role(role_id):
    data = request.json
    updated_role = update_role(role_id, data)
    if not updated_role:
        return jsonify({"message": "Role not found"}), 404
    return jsonify(updated_role), 200
# Route để xóa vai trò
@role_bp.route('/roles/<int:role_id>', methods=['DELETE'])
def delete_existing_role(role_id):
    success = delete_role(role_id)
    if not success:
        return jsonify({"message": "Role not found"}), 404
    return jsonify({"message": "Role deleted successfully"}), 200