import firebase_admin
from firebase_admin import credentials, db
import datetime
def upload_notification_to_firebase(data):
    try:
        # Tạo dữ liệu thông báo với tên người gửi, nội dung và trạng thái
        notification_data = {
            "sender": data["sender_name"],
            "message": data["message_content"],
            "timestamp": datetime.datetime.now().isoformat(),  # Thêm thời gian gửi thông báo
            "status": "pending" ,
            "type": data["type"],   # Thêm thời gian gửi thông báo
        }
        
        # Tham chiếu đến node thông báo trong database
        ref = db.reference('/notifications')  # Thay đổi node để lưu thông báo
        new_ref = ref.push(notification_data)  # Đẩy dữ liệu thông báo lên Firebase
        
        return new_ref.key  # Trả về ID của bản ghi thông báo mới
    except Exception as e:
        raise Exception(f"Error uploading notification to Firebase: {str(e)}")
    
    # Function to update the status of a notification
def update_notification_status(notification_id, new_status):
    try:
        # Tham chiếu đến thông báo cần cập nhật bằng ID
        ref = db.reference(f'/notifications/{notification_id}')
        
        # Kiểm tra trạng thái mới hợp lệ
        valid_statuses = ["pending", "approved", "rejected"]
        if new_status not in valid_statuses:
            raise ValueError("Invalid status. Status must be one of: 'pending', 'approved', 'rejected'.")
        # Cập nhật trạng thái cho thông báo
        ref.update({
            "status": new_status
        })
        return True  # Trả về True nếu cập nhật thành công
    except Exception as e:
        raise Exception(f"Error updating notification status: {str(e)}")