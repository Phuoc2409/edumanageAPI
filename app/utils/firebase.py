import firebase_admin
from firebase_admin import credentials, auth, firestore

def initialize_firebase():
    # Đọc file JSON cấu hình
    cred = credentials.Certificate("path/to/your/firebase-private-key.json")
    
    # Khởi tạo Firebase Admin SDK
    firebase_admin.initialize_app(cred)

    # Khởi tạo Firestore
    db = firestore.client()
    
    # Bạn có thể thực hiện các thao tác với Firestore hoặc Authentication ở đây
    return db
