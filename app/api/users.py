from flask import Blueprint, request, jsonify
from ..services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user
)

users_bp = Blueprint('users_bp', __name__)

# Route để lấy danh sách tất cả người dùng
@users_bp.route('/users', methods=['GET'])
def list_users():
    users = get_all_users()
    return jsonify(users), 200


# Route để lấy thông tin chi tiết người dùng
@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user), 200


# Route để tạo mới người dùng
@users_bp.route('/users', methods=['POST'])
def create_new_user():
    data = request.json
    required_fields = ["fullname", "gmail", "phonenumber", "username", "password"]
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    new_user = create_user(data)
    return jsonify(new_user), 201


# Route để cập nhật người dùng
@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_existing_user(user_id):
    data = request.json
    updated_user = update_user(user_id, data)
    if not updated_user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(updated_user), 200


# Route để xóa người dùng
@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_existing_user(user_id):
    success = delete_user(user_id)
    if not success:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"}), 200
