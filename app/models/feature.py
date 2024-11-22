from ..database import db

class Feature(db.Model):
    __tablename__ = 'features'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=True)
    
    feature_type_id = db.Column(db.Integer, db.ForeignKey('feature_types.id'), nullable=False)
    feature_type = db.relationship('FeatureType', backref='features', lazy=True)
    deleted_at = db.Column(db.Date)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "feature_type": self.feature_type.name
        }
