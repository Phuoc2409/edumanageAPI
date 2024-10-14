from flask import Flask
from .database import db
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/edumanage'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'key_is_key'
    jwt = JWTManager(app)

    db.init_app(app)

    with app.app_context():
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
