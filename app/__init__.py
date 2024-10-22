from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

import os

# Khởi tạo các đối tượng toàn cục
db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mssql+pyodbc://@MSI\\SQLEXPRESS/edumanage?driver=ODBC+Driver+17+for+SQL+Server')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'key_is_key')

    # Khởi tạo các phần mở rộng
    db.init_app(app)
    jwt.init_app(app)
   

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

    return app
