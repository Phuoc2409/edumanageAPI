from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from app.database import db

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        # Tạo token cho người dùng
        access_token = create_access_token(identity=user.id)
        return access_token
    return None

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
