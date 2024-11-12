from ..database import db

class AssetDetail(db.Model):
    __tablename__ = 'asset_details'  # Tên bảng trong cơ sở dữ liệu

    # Các thuộc tính của model
    id = db.Column(db.Integer, primary_key=True)  # Khóa chính
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    identifier_number = db.Column(db.Text, nullable=False)  # Số hiệu tài sản
    user_id = db.Column(db.Integer, nullable=False)  # ID người dùng
    purchase_date = db.Column(db.Date, nullable=False)  # Ngày mua
    purchase_price = db.Column(db.Float, nullable=False)  # Giá mua
    used_years = db.Column(db.Integer, nullable=False)  # Số năm đã sử dụng
    last_maintenance_date = db.Column(db.Date, nullable=False)  # Ngày bảo trì cuối
    parent_id = db.Column(db.Integer, nullable=False) 
    status = db.Column(db.Text, nullable=False)  # Trạng thái tài sản

    asset = db.relationship("Asset", back_populates="asset_details")

    def to_dict(self):
        return {
            "id": self.id,
            "identifier_number": self.identifier_number,
            "user_id": self.user_id,
            "purchase_date": str(self.purchase_date),
            "purchase_price": self.purchase_price,
            "used_years": self.used_years,
            "last_maintenance_date": str(self.last_maintenance_date),
            "status": self.status,
            "asset_id": self.asset_id,
            "parent_id":self.asset_id,
            "asset": {
                "id": self.asset.id,
                "name": self.asset.asset_name,
                "description": self.asset.description
            } if self.asset else None        
        }
