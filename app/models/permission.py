from ..database import db  

class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)  

    def to_dict(self):
        return {
            "id": self.id,
            "permission_name": self.permission_name,
            "description": self.description,
        }
