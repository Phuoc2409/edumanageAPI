import os

class Config:
 # Cấu hình kết nối đến MySQL trên WampServer
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/edumanage'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
