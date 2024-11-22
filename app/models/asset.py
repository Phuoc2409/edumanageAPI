from ..database import db

class Asset(db.Model):
    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    deleted_at = db.Column(db.Date)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', backref='assets', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "asset_name": self.asset_name,
            "description": self.description,
            "category": self.category.name if self.category else None
        }


