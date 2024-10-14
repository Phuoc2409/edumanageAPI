from app import create_app
from flask_cors import CORS

# Tạo ứng dụng Flask
app = create_app()

# Cấu hình CORS cho ứng dụng
CORS(app)  # Cho phép tất cả các nguồn, có thể chỉ định các nguồn cụ thể nếu cần

if __name__ == "__main__":
    # Chạy ứng dụng trên cổng 2409 với chế độ debug
    app.run(host='0.0.0.0',port=2409, debug=True)
