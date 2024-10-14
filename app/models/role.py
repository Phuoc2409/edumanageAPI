from ..database import db  

class Role(db.Model):
    __tablename__ = 'roles'  # Tên bảng trong cơ sở dữ liệu

    # Các thuộc tính của model
    id = db.Column(db.Integer, primary_key=True)  # Khóa chính
    role_name = db.Column(db.Text, nullable=False)  # Tên vai trò
    description = db.Column(db.Text, nullable=False)  # Mô tả vai trò


    def to_dict(self):
        return {
            "id": self.id,
            "role_name": self.role_name,
            "description": self.description,
        }
