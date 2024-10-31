from ..database import db

class AssetFeature(db.Model):
    __tablename__ = 'asset_features'  # Tên bảng trong cơ sở dữ liệu

    # Các thuộc tính của model
    id = db.Column(db.Integer, primary_key=True)  # Khóa chính
    asset_feature_name = db.Column(db.Text, nullable=False)  # Tên đặc điểm tài sản
    description = db.Column(db.Text, nullable=False)  # Mô tả đặc điểm
    
    def to_dict(self):
        return {
            "id": self.id,
            "asset_feature_name": self.asset_feature_name,
            "description": self.description,
        }
