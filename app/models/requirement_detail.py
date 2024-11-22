from ..database import db

class RequirementDetail(db.Model):
    __tablename__ = 'requirement_details'  # Tên bảng trong cơ sở dữ liệu

    # Các thuộc tính của model
    id = db.Column(db.Integer, primary_key=True)  # Khóa chính
    asset_detail_id = db.Column(db.Integer, nullable=False)  # ID chi tiết tài sản
    requirement_type = db.Column(db.String(50), nullable=False)  # Loại yêu cầu
    description = db.Column(db.Text, nullable=False)  # Mô tả chi tiết yêu cầu
    deleted_at = db.Column(db.Date)

    def to_dict(self):
        return {
            "id": self.id,
            "asset_detail_id": self.asset_detail_id,
            "requirement_type": self.requirement_type,
            "description": self.description,
            "deleted_at":self.deleted_at
        }
