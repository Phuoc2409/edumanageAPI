from ..database import db

class RolePermission(db.Model):
    __tablename__ = 'role_permission'  # Tên bảng trong cơ sở dữ liệu

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID chính, tự động tăng
    role_id = db.Column(db.Integer, nullable=False)  # ID của vai trò
    permission_id = db.Column(db.Integer, nullable=False)  # ID của quyền

    def __repr__(self):
        return f'<RolePermission role_id={self.role_id} permission_id={self.permission_id}>'
