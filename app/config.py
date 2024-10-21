import os

class Config:
 # Cấu hình kết nối đến MySQL trên WampServer
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mssql+pyodbc://@MSI\\SQLEXPRESS/edumanage?driver=ODBC+Driver+17+for+SQL+Server')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
