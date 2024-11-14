import firebase_admin
from firebase_admin import credentials, db
import datetime
def upload_notification_to_firebase(data):
    try:
        # Tạo dữ liệu thông báo với tên người gửi và nội dung
        notification_data = {
            "sender": data["sender_name"],
            "message": data["message_content"],
            "timestamp": datetime.datetime.now().isoformat()  # Thêm thời gian gửi thông báo
        }
        
        # Tham chiếu đến node thông báo trong database
        ref = db.reference('/notifications')  # Thay đổi node để lưu thông báo
        new_ref = ref.push(notification_data)  # Đẩy dữ liệu thông báo lên Firebase
        
        return new_ref.key  # Trả về ID của bản ghi thông báo mới
    except Exception as e:
        raise Exception(f"Error uploading notification to Firebase: {str(e)}")
