from app.models.user import User
from app.database import db
from app.models.user import User
from app.models.user_role import UserRole
from app.models.role import Role
from ..database import db
from ..models.user import User
from ..models.role import Role
from ..models.user_role import UserRole
from werkzeug.security import check_password_hash, generate_password_hash
def create_user(data):
    """
    Tạo người dùng mới.
    """
    new_user = User(
        fullname=data.get("fullname"),
        gmail=data.get("gmail"),
        password=generate_password_hash(data.get("password")),
        phonenumber=data.get("phonenumber"),
        username=data.get("username")
        
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


def search_users_service(filters):

    fullname = filters.get('fullname', None)
    gmail = filters.get('gmail', None)
    phonenumber = filters.get('phonenumber', None)
    role_name = filters.get('roles', None)
    username = filters.get('username', None)
    # Truy vấn cơ bản
    query = db.session.query(
        User,
        Role.role_name
    ).join(
        UserRole, User.id == UserRole.user_id
    ).join(
        Role, UserRole.role_id == Role.id
    )

    # Áp dụng bộ lọc
    if fullname:
        query = query.filter(User.fullname.ilike(f"%{fullname}%"))
    if gmail:
        query = query.filter(User.gmail.ilike(f"%{gmail}%"))
    if phonenumber:
        query = query.filter(User.phonenumber.like(f"%{phonenumber}%"))
    if role_name:
        query = query.filter(Role.role_name.ilike(f"%{role_name}%"))
    if username:
        query = query.filter(User.username.ilike(f"%{username}%"))
    # Thực hiện truy vấn
    users = query.all()

    # Xử lý dữ liệu
    result = {}
    for user, role_name in users:
        user_id = user.id
        if user_id not in result:
            result[user_id] = {
                "id": user.id,
                "fullname": user.fullname,
                "gmail": user.gmail,
                "phonenumber": user.phonenumber,
                "username": user.username,
                "roles": []
            }
        if role_name not in result[user_id]["roles"]:
            result[user_id]["roles"].append(role_name)

    return list(result.values())