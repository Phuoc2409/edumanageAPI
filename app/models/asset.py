from ..database import db

class Asset(db.Model):
    __tablename__ = 'assets'  # Tên bảng trong cơ sở dữ liệu

    # Các thuộc tính của model
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', backref='assets', lazy=True)
    deleted_at = db.Column(db.Date, nullable=True)
    def to_dict(self):
        return {
            "id": self.id,
            "asset_name": self.asset_name,
            "description": self.description,
            "category": self.category.name if self.category else None,
            "deleted_at":self.deleted_at
        }
