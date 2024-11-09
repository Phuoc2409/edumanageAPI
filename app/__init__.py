from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.database import db
import firebase_admin
from firebase_admin import initialize_app,credentials, db as firebase_db # Hoặc db nếu bạn dùng Firebase Realtime Database
import boto3
import json
import os
from datetime import timedelta

# Khởi tạo các đối tượng toàn cục

jwt = JWTManager()

def get_firebase_credentials():
    secrets_client = boto3.client(
        'secretsmanager',
        region_name='us-east-1',  # Bạn có thể giữ nguyên hoặc thay đổi tùy vào setup
        endpoint_url='http://18.142.186.91:3000'  # URL tùy chỉnh của bạn
    )
    secret_name = 'firebase/credentials'

    # Truy xuất secret từ endpoint tùy chỉnh
    secret_value = secrets_client.get_secret_value(SecretId=secret_name)
    firebase_credentials_json = secret_value['SecretString']

    # Chuyển đổi từ JSON sang dict
    firebase_credentials = json.loads(firebase_credentials_json)
    return firebase_credentials

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'mysql+pymysql://root:@localhost/edumanage')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'key_is_key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)  # Thời gian sống của access token
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30) 
    # Khởi tạo các phần mở rộng
    db.init_app(app)
    jwt.init_app(app)
   
    firebase_credentials = get_firebase_credentials()
    cred = credentials.Certificate(firebase_credentials)
    initialize_app(cred, {
        'databaseURL': 'https://edumange-fdfeb-default-rtdb.firebaseio.com/' 
    })
    firebase_realtime_db = firebase_db.reference()  # Tham chiếu gốc tới Realtime Database


    # cred = credentials.Certificate("D:\Download\edumage-realtime-db-key.json")  # Thay path/to/your-firebase-adminsdk.json bằng đường dẫn thật của file JSON
    # firebase_admin.initialize_app(cred)

    # firebase_db = firebase_admin.db.reference()  # Khởi tạo với URL của Database



    with app.app_context():
        # Import blueprints
        from .api.users import users_bp
        from .api.auth import auth_bp
        from .api.asset import assets_bp
        from .api.asset_detail import asset_details_bp
        from .api.asset_feature import asset_features_bp
        from .api.feature import features_bp
        from .api.feature_type import feature_types_bp
        from .api.category import categories_bp
        from .api.requirement import requirements_bp
        from .api.requirement_detail import requirement_details_bp

        api_prefix = '/api'

        blueprints = [
            (auth_bp, 'auth'),
            (users_bp, ''),
            (assets_bp, ''),
            (asset_details_bp, ''),
            (asset_features_bp, ''),
            (features_bp, ''),
            (feature_types_bp, ''),
            (categories_bp, ''),
            (requirements_bp, ''),
            (requirement_details_bp, ''),
        ]

        # Đăng ký các blueprint với prefix chung
        for bp, path in blueprints:
            app.register_blueprint(bp, url_prefix=f'{api_prefix}/{path}' if path else api_prefix)

    app.firebase_realtime_db = firebase_realtime_db

    return app
