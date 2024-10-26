# Sử dụng Python image
FROM python:3.9-slim

# Cài đặt các dependency
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy toàn bộ mã nguồn vào Docker container
COPY . .

# Thiết lập cổng mà app sẽ lắng nghe
EXPOSE 3000

# Chạy app
CMD ["python", "main.py"]