from ..database import db
from ..models.permission import Permission
def create_permission(data):
    """
    Tạo một quyền mới.
    """
    new_permission = Permission(
        permission_name=data.get("permission_name"),
        description=data.get("description")
    )
    db.session.add(new_permission)
    db.session.commit()
    return new_permission.to_dict()
def get_all_permissions():
    """
    Lấy danh sách tất cả quyền.
    """
    permissions = Permission.query.all()
    return [permission.to_dict() for permission in permissions]
def get_permission_by_id(permission_id):
    """
    Lấy chi tiết quyền theo ID.
    """
    permission = Permission.query.get(permission_id)
    if permission:
        return permission.to_dict()
    return None
def update_permission(permission_id, data):
    """
    Cập nhật thông tin quyền.
    """
    permission = Permission.query.get(permission_id)
    if not permission:
        return None
    permission.permission_name = data.get("permission_name", permission.permission_name)
    permission.description = data.get("description", permission.description)
    db.session.commit()
    return permission.to_dict()
def delete_permission(permission_id):
    """
    Xóa một quyền.
    """
    permission = Permission.query.get(permission_id)
    if not permission:
        return False
    db.session.delete(permission)
    db.session.commit()
    return True