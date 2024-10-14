from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity  # Nếu dùng JWT
from app.models.user import User
from app.models.user_role import UserRole
from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission

def permission_required(permission_name):
    def decorator(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()  # Lấy user_id từ token
            user = User.query.get(current_user_id)

            if not user:
                return jsonify({'message': 'User not found'}), 404

            if not user_has_permission(user, permission_name):
                return jsonify({'message': 'Permission denied'}), 403

            return fn(*args, **kwargs)
        return decorated_function
    return decorator

def user_has_permission(user, permission_name):
    for permission in get_user_permissions(user.id):
        if permission == permission_name:
            return True
    return False
def get_user_permissions(user_id):
    user_roles = UserRole.query.filter_by(user_id=user_id).all()
    
    permissions = set()  

    for user_role in user_roles:
        role = Role.query.get(user_role.role_id)
        role_permissions = RolePermission.query.filter_by(role_id=role.id).all()
        
        for role_permission in role_permissions:
            permission = Permission.query.get(role_permission.permission_id)
            permissions.add(permission.permission_name)

    return list(permissions)
