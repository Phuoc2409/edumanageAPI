from ..database import db

class AssetDetail(db.Model):
    __tablename__ = 'asset_details'

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    identifier_number = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    purchase_date = db.Column(db.Date, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    used_years = db.Column(db.Integer, nullable=False)
    last_maintenance_date = db.Column(db.Date, nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('asset_details.id'), nullable=True)
    status = db.Column(db.Enum('available', 'in_use', 'under_maintenance', 'disposed'), nullable=False)
    deleted_at = db.Column(db.Date, nullable=True)
    asset = db.relationship('Asset', backref='asset_details', lazy=True)
    user = db.relationship('User', backref='asset_details', lazy=True)
    parent = db.relationship('AssetDetail', remote_side=[id], backref='children', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "asset": self.asset.asset_name if self.asset else None,
            "identifier_number": self.identifier_number,
            "user": self.user.fullname if self.user else None,
            "purchase_date": self.purchase_date,
            "purchase_price": self.purchase_price,
            "used_years": self.used_years,
            "last_maintenance_date": self.last_maintenance_date,
            "parent_id": self.parent_id,
            "status": self.status,
            "deleted_at":self.deleted_at
        }
