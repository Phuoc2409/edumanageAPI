# app/models/user.py

from ..database import db  # Sửa import để đảm bảo đường dẫn đúng

class User(db.Model):
    __tablename__ = 'users'  # Tên bảng trong cơ sở dữ liệu

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID chính
    fullname = db.Column(db.Text, nullable=False)  # Tên
    gmail = db.Column(db.Text, nullable=False)  # Gmail - Đã sửa từ LongText thành Text
    phonenumber = db.Column(db.Integer, nullable=False)  # Số điện thoại
    username = db.Column(db.Text, nullable=False)  # Tên đăng nhập - Đã sửa từ LongText thành Text
    password = db.Column(db.Text, nullable=False)  # Mật khẩu - Đã sửa từ LongText thành Text
    deleted_at = db.Column(db.Date)
    def to_dict(self):
        return {
            'id': self.id,
            'fullname': self.fullname,
            'gmail': self.gmail,
            'phonenumber': self.phonenumber,
            'username': self.username,
            'password': self.password,
            'deleted_at': self.deleted_at,
        }
