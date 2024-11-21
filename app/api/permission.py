from flask import Blueprint, request, jsonify
from ..services.permission_service import (
    create_permission,
    get_all_permissions,
    get_permission_by_id,
    update_permission,
    delete_permission
)

permission_bp = Blueprint('permission_bp', __name__)

# Route để lấy danh sách tất cả quyền
@permission_bp.route('/permissions', methods=['GET'])
def list_permissions():
    permissions = get_all_permissions()
    return jsonify(permissions), 200


# Route để lấy thông tin chi tiết quyền
@permission_bp.route('/permissions/<int:permission_id>', methods=['GET'])
def get_permission(permission_id):
    permission = get_permission_by_id(permission_id)
    if not permission:
        return jsonify({"message": "Permission not found"}), 404
    return jsonify(permission), 200


# Route để tạo mới quyền
@permission_bp.route('/permissions', methods=['POST'])
def create_new_permission():
    data = request.json
    if not data or "permission_name" not in data or "description" not in data:
        return jsonify({"message": "Missing required fields"}), 400

    new_permission = create_permission(data)
    return jsonify(new_permission), 201


# Route để cập nhật quyền
@permission_bp.route('/permissions/<int:permission_id>', methods=['PUT'])
def update_existing_permission(permission_id):
    data = request.json
    updated_permission = update_permission(permission_id, data)
    if not updated_permission:
        return jsonify({"message": "Permission not found"}), 404
    return jsonify(updated_permission), 200


# Route để xóa quyền
@permission_bp.route('/permissions/<int:permission_id>', methods=['DELETE'])
def delete_existing_permission(permission_id):
    success = delete_permission(permission_id)
    if not success:
        return jsonify({"message": "Permission not found"}), 404
    return jsonify({"message": "Permission deleted successfully"}), 200
