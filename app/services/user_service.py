from app.models.user import User
from app.database import db

def create_user(user_data):
    user = User(
        fullname=user_data['fullname'],
        gmail=user_data['gmail'],
        phonenumber=user_data['phonenumber'],
        username=user_data['username'],
        password=user_data['password']
    )
    db.session.add(user)
    db.session.commit()
    return user.to_dict() 

def get_user_by_id(user_id):
    return User.query.get(user_id).to_dict() if User.query.get(user_id) else None 
