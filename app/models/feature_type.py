from ..database import db

class FeatureType(db.Model):
    __tablename__ = 'feature_types'  # Tên bảng trong cơ sở dữ liệu

    # Các thuộc tính của model
    id = db.Column(db.Integer, primary_key=True)  # Khóa chính
    name = db.Column(db.Text, nullable=False)  # Tên loại đặc điểm
    description = db.Column(db.Text, nullable=False)  # Mô tả loại đặc điểm

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }
