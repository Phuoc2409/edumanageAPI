from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.database import db
import firebase_admin
from firebase_admin import initialize_app, credentials, db as firebase_db
import os
from datetime import timedelta

# Khởi tạo các đối tượng toàn cục
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:123456@18.142.186.91/edumanage'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'key_is_key_really_256bit_long_example_here')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

    # Khởi tạo SQLAlchemy và JWT
    db.init_app(app)
    jwt.init_app(app)

    # Khởi tạo Firebase với đường dẫn tệp key đã tải lên AWS
    firebase_key_path = "/etc/secrets/edumage-realtime-db-key.json"

    cred = credentials.Certificate(firebase_key_path)
    firebase_app = initialize_app(cred, {
        'databaseURL': 'https://edumange-fdfeb-default-rtdb.firebaseio.com/'
    })
    firebase_realtime_db = firebase_db.reference()  # Tham chiếu gốc tới Realtime Database

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
        from .api.firebase import firebase_bp
        from .api.permission import permission_bp
        from .api.role import role_bp

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
            (permission_bp, ''),
            (role_bp, ''),
            (firebase_bp,''),
        ]

        # Đăng ký các blueprint với prefix chung
        for bp, path in blueprints:
            app.register_blueprint(bp, url_prefix=f'{api_prefix}/{path}' if path else api_prefix)

    # Đưa Firebase Realtime Database reference vào app context
    app.firebase_realtime_db = firebase_realtime_db

    return app
