import os

class Config:
 # Cấu hình kết nối đến MySQL trên WampServer
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
    'mysql+pymysql://root:123456@18.142.186.91/edumanage')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
