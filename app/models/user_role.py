from ..database import db

class UserRole(db.Model):
    __tablename__ = 'user_role'  # Tên bảng trong cơ sở dữ liệu

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID chính, tự động tăng
    user_id = db.Column(db.Integer, nullable=False)  # ID của người dùng
    role_id = db.Column(db.Integer, nullable=False)  # ID của vai trò
   

    def __repr__(self):
        return f'<UserRole user_id={self.user_id} role_id={self.role_id}>'
