from ..database import db

class Asset(db.Model):
    __tablename__ = 'assets'  # Tên bảng trong cơ sở dữ liệu

    # Các thuộc tính của model
    id = db.Column(db.Integer, primary_key=True)  # Khóa chính
    asset_name = db.Column(db.Text, nullable=False)  # Tên tài sản
    description = db.Column(db.Text, nullable=False)  # Mô tả tài sản
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)  # Khóa ngoại đến bảng categories

    def to_dict(self):
        return {
            "id": self.id,
            "asset_name": self.asset_name,
            "description": self.description,
            "category_id": self.category_id,
        }
