from app import create_app
from flask_cors import CORS
import os
# Tạo ứng dụng Flask
app = create_app()

# Cấu hình CORS cho ứng dụng
CORS(app, resources={r"/api/*": {"origins": "https://back-end-edu-1303b043ad7c.herokuapp.com"}})  # Cho phép tất cả các nguồn, có thể chỉ định các nguồn cụ thể nếu cần

if __name__ == "__main__":
    # Chạy ứng dụng trên cổng 2409 với chế độ debug
    port = int(os.getenv('PORT', 2409))  # Heroku will set PORT, fallback to 2409 if running locally
    app.run(host='0.0.0.0', port=port, debug=True)
