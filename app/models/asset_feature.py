from ..database import db

class AssetFeature(db.Model):
    __tablename__ = 'asset_features'  # Tên bảng trong cơ sở dữ liệu

    # Các thuộc tính của model
    id = db.Column(db.Integer, primary_key=True)  # Khóa chính
    asset_detail_id = db.Column(db.Integer, nullable=False) 
    feature_id = db.Column(db.Integer, nullable=False)  # Tên đặc điểm tài sản
    description = db.Column(db.Text, nullable=False)  # Mô tả đặc điểm
    
    def to_dict(self):
        return {
            "id": self.id,
            "asset_detail_id": self.asset_detail_id,
            "feature_id":self.feature_id,
            "description": self.description,
        }
