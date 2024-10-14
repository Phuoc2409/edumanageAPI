from ..database import db

class Category(db.Model):
    __tablename__ = 'categories'  # Tên bảng trong cơ sở dữ liệu

    # Các thuộc tính của model
    id = db.Column(db.Integer, primary_key=True)  # Khóa chính
    name = db.Column(db.Text, nullable=False)  # Tên danh mục
    description = db.Column(db.Text, nullable=False)  # Mô tả danh mục
    min_lifespan = db.Column(db.Integer, nullable=False)  # Tuổi thọ tối thiểu
    max_lifespan = db.Column(db.Integer, nullable=False)  # Tuổi thọ tối đa
    default_salvage_value_rate = db.Column(db.Float, nullable=False)  # Tỷ lệ giá trị thanh lý mặc định
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)  # Khóa ngoại đến bảng categories

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "min_lifespan": self.min_lifespan,
            "max_lifespan": self.max_lifespan,
            "default_salvage_value_rate": self.default_salvage_value_rate,
            "parent_id": self.parent_id,
        }
