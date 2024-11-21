from ..database import db
from ..models.user import User


def create_user(data):
    """
    Tạo người dùng mới.
    """
    new_user = User(
        fullname=data.get("fullname"),
        gmail=data.get("gmail"),
        phonenumber=data.get("phonenumber"),
        username=data.get("username"),
        password=data.get("password")
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user.to_dict()


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
