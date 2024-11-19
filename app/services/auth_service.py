from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity
from app.models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from app.database import db
from datetime import timedelta

def generate_tokens(user_id):
    # Tạo access_token với thời gian sống ngắn (15 phút)
    access_token = create_access_token(identity=str(user_id), expires_delta=timedelta(minutes=15))

    # Tạo refresh_token với thời gian sống lâu hơn (30 ngày)
    refresh_token = create_refresh_token(identity=str(user_id), expires_delta=timedelta(days=30))

    return access_token, refresh_token

@jwt_required()
def logout_user(response):
    # Xử lý đăng xuất (tùy theo cách bạn xử lý token)
    return response

@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()  # Lấy user_id từ token
    return User.query.get(current_user_id)

def register_user(username, password, fullname, gmail, phonenumber):
    # Kiểm tra xem người dùng đã tồn tại chưa
    if User.query.filter_by(username=username).first():
        return None  

    # Tạo người dùng mới
    new_user = User(
        username=username,
        password=generate_password_hash(password),  # Mã hóa mật khẩu
        fullname=fullname,
        gmail=gmail,
        phonenumber=phonenumber
    )
    
    db.session.add(new_user)
    db.session.commit()

    return new_user  # Trả về người dùng mới được tạo
