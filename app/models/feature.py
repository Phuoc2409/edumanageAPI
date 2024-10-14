from ..database import db

class Feature(db.Model):
    __tablename__ = 'features'  # Tên bảng trong cơ sở dữ liệu

    # Các thuộc tính của model
    id = db.Column(db.Integer, primary_key=True)  # Khóa chính
    ordinal_number = db.Column(db.Integer, nullable=False)  # Số thứ tự
    description = db.Column(db.Text, nullable=False)  # Mô tả

    def to_dict(self):
        return {
            "id": self.id,
            "ordinal_number": self.ordinal_number,
            "description": self.description,
        }
