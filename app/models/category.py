from ..database import db

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    min_lifespan = db.Column(db.Integer, nullable=False)
    max_lifespan = db.Column(db.Integer, nullable=False)
    default_salvage_value_rate = db.Column(db.Float, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    parent = db.relationship('Category', remote_side=[id], backref='subcategories', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "min_lifespan": self.min_lifespan,
            "max_lifespan": self.max_lifespan,
            "default_salvage_value_rate": self.default_salvage_value_rate,
            "parent_id": self.parent_id
        }
