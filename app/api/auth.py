from flask import Blueprint, request, jsonify
from app.services.auth_service import login_user, logout_user, get_current_user, register_user
from flask_jwt_extended import jwt_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    print(username + ' ' +password)
    token = login_user(username, password)

    if token:
        return jsonify(access_token=token), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'message': 'Successfully logged out'})
    return logout_user(response)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    fullname = data.get('fullname')
    gmail = data.get('gmail')
    phonenumber = data.get('phonenumber')

    # Gọi hàm register_user từ auth_service
    new_user = register_user(username, password, fullname, gmail, phonenumber)

    if new_user:
        return jsonify({'message': 'User registered successfully'}), 201
    else:
        return jsonify({'message': 'Username already exists'}), 400

@auth_bp.route('/user/profile', methods=['GET'])
@jwt_required()
def user_profile():
    user = get_current_user()
    
    if user:
        return jsonify({'username': user.username, 'email': user.gmail}), 200
    else:
        return jsonify({'message': 'User not found'}), 404
