from ..database import db

class Requirement(db.Model):
    __tablename__ = 'requirements'  # Tên bảng trong cơ sở dữ liệu

    # Các thuộc tính của model
    id = db.Column(db.Integer, primary_key=True)  # Khóa chính
    user_id = db.Column(db.Integer, nullable=False)  # ID người dùng
    requester_identifier = db.Column(db.String(100), nullable=False)  # ID yêu cầu
    date = db.Column(db.DateTime, nullable=False)  # Ngày yêu cầu
    description = db.Column(db.Text, nullable=False)  # Mô tả yêu cầu
    status = db.Column(db.String(50), nullable=False)  # Trạng thái yêu cầu

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "requester_identifier": self.requester_identifier,
            "date": self.date.isoformat(),
            "description": self.description,
            "status": self.status,
        }
