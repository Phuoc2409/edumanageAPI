from flask import Blueprint, request, jsonify
from app.services.auth_service import  logout_user, get_current_user, register_user
from flask_jwt_extended import jwt_required
from app.models.user import User  # Lấy model người dùng từ database
from app.services.auth_service import generate_tokens  # Chúng ta sẽ gọi hàm này để tạo token
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    
    # Kiểm tra username và password từ database
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        # Tạo access_token và refresh_token
        access_token, refresh_token = generate_tokens(user.id)
        
        # Trả về cả access_token và refresh_token
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401
    
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  # Yêu cầu người dùng phải cung cấp refresh_token
def refresh():
    current_user = get_jwt_identity()  # Lấy user_id từ refresh_token
    new_access_token = create_access_token(identity=current_user)  # Tạo access_token mới
    return jsonify(access_token=new_access_token), 200

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
