from ..database import db
from ..models.user import User
from ..models.role import Role
from ..models.user_role import UserRole
from werkzeug.security import  generate_password_hash

def create_user(data):
    """
    Tạo người dùng mới và thêm vai trò cho họ.
    """
    # Tạo người dùng mới
    new_user = User(
        fullname=data.get("fullname"),
        gmail=data.get("gmail"),
        phonenumber=data.get("phonenumber"),
        username=data.get("username"),
        password=generate_password_hash(data.get("password")),  # Mã hóa mật khẩu
    )
    db.session.add(new_user)
    db.session.flush()  # Đảm bảo new_user.id được gán sau khi thêm vào session

    # Thêm vai trò vào bảng user_role
    roles = data.get("roles", [])  # Lấy danh sách role_id từ request, mặc định là danh sách rỗng
    for role_id in roles:
        role = Role.query.get(role_id)
        if not role:
            continue  # Bỏ qua nếu role_id không tồn tại

        user_role = UserRole(user_id=new_user.id, role_id=role_id)
        db.session.add(user_role)

    db.session.commit()

    return {
        "user": new_user.to_dict(),
        "roles": [role.to_dict() for role in Role.query.filter(Role.id.in_(roles)).all()]
    }

def get_all_users():
    """
    Lấy danh sách tất cả người dùng.
    """
    users = User.query.all()
    return [user.to_dict() for user in users]


def get_user_by_id(user_id):
    """
    Lấy thông tin người dùng theo ID.
    """
    user = User.query.get(user_id)
    if user:
        return user.to_dict()
    return None


def update_user(user_id, data):
    """
    Cập nhật thông tin người dùng.
    """
    user = User.query.get(user_id)
    if not user:
        return None

    user.fullname = data.get("fullname", user.fullname)
    user.gmail = data.get("gmail", user.gmail)
    user.phonenumber = data.get("phonenumber", user.phonenumber)
    user.username = data.get("username", user.username)
    user.password = data.get("password", user.password)
    user.deleted_at = data.get("deleted_at", user.deleted_at)

    db.session.commit()
    return user.to_dict()


def delete_user(user_id):
    """
    Xóa một người dùng.
    """
    user = User.query.get(user_id)
    if not user:
        return False

    db.session.delete(user)
    db.session.commit()
    return True
