from flask import Blueprint, jsonify, request
from app.services.user_service import create_user, get_user_by_id
from app.utils.permisions import permission_required
from flask_jwt_extended import jwt_required

# Tạo một blueprint để định nghĩa API liên quan đến users
users_bp = Blueprint("users", __name__)

# Tạo người dùng mới
@permission_required('user-add')  
@users_bp.route("/users", methods=["POST"])
def add_user():
    user_data = request.get_json()
    user = create_user(user_data)
    return jsonify(user), 201

# Lấy thông tin người dùng theo ID
@users_bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required() 
@permission_required('user-index') 
def read_user(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200
