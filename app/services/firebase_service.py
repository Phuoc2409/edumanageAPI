import firebase_admin
from firebase_admin import credentials, db
def upload_to_firebase(data):
    try:
        # Tham chiếu đến node trong database
        ref = db.reference('/user')
        new_ref = ref.push(data)  # Đẩy dữ liệu lên Firebase
        return new_ref.key  # Trả về ID của bản ghi mới
    except Exception as e:
        raise Exception(f"Error uploading data to Firebase: {str(e)}")