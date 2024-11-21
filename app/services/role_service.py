from ..database import db
from ..models.role import Role


def create_role(data):
    """
    Tạo một vai trò mới.
    """
    new_role = Role(
        role_name=data.get("role_name"),
        description=data.get("description")
    )
    db.session.add(new_role)
    db.session.commit()
    return new_role.to_dict()


def get_all_roles():
    """
    Lấy danh sách tất cả vai trò.
    """
    roles = Role.query.all()
    return [role.to_dict() for role in roles]


def get_role_by_id(role_id):
    """
    Lấy chi tiết vai trò theo ID.
    """
    role = Role.query.get(role_id)
    if role:
        return role.to_dict()
    return None


def update_role(role_id, data):
    """
    Cập nhật thông tin vai trò.
    """
    role = Role.query.get(role_id)
    if not role:
        return None

    role.role_name = data.get("role_name", role.role_name)
    role.description = data.get("description", role.description)

    db.session.commit()
    return role.to_dict()


def delete_role(role_id):
    """
    Xóa một vai trò.
    """
    role = Role.query.get(role_id)
    if not role:
        return False

    db.session.delete(role)
    db.session.commit()
    return True
