from ..database import db

class FeatureType(db.Model):
    __tablename__ = 'feature_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    deleted_at = db.Column(db.Date)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "deleted_at":self.deleted_at
        }
