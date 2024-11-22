from ..database import db

class AssetFeature(db.Model):
    __tablename__ = 'asset_features'

    id = db.Column(db.Integer, primary_key=True)
    asset_detail_id = db.Column(db.Integer, db.ForeignKey('asset_details.id'), nullable=False)
    feature_id = db.Column(db.Integer, db.ForeignKey('features.id'), nullable=False)
    description = db.Column(db.Text, nullable=True)

    asset_detail = db.relationship('AssetDetail', backref='features', lazy=True)
    feature = db.relationship('Feature', backref='asset_features', lazy=True)
    deleted_at = db.Column(db.Date)

    def to_dict(self):
        return {
            "id": self.id,
            "asset_detail_id": self.asset_detail_id,
            "feature": self.feature.name if self.feature else None,
            "description": self.description,
            "deleted_at":self.deleted_at
        }

