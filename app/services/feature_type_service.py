from app.models.feature_type import FeatureType
from app.database import db
from app.models.feature import Feature

def create_feature_type(feature_type_data):
    feature_type = FeatureType(
        name=feature_type_data['name'],
        description=feature_type_data['description']
    )
    db.session.add(feature_type)
    db.session.commit()
    return feature_type.to_dict()

def get_feature_type_by_id(feature_type_id):
    return FeatureType.query.get(feature_type_id).to_dict() if FeatureType.query.get(feature_type_id) else None

def get_all_feature_types():
    return [feature_type.to_dict() for feature_type in FeatureType.query.all()]

def update_feature_type(feature_type_id, feature_type_data):
    feature_type = FeatureType.query.get(feature_type_id)
    if feature_type:
        feature_type.name = feature_type_data.get('name', feature_type.name)
        feature_type.description = feature_type_data.get('description', feature_type.description)
        feature_type.deleted_at = feature_type_data.get('deleted_at', feature_type.deleted_at)
        db.session.commit()
        return feature_type.to_dict()
    return None

def delete_feature_type(feature_type_id):
    feature_type = FeatureType.query.get(feature_type_id)
    if feature_type:
        db.session.delete(feature_type)
        db.session.commit()
        return True
    return False

def get_feature_with_type(feature_id):
    # Tìm Feature theo ID
    feature = Feature.query.get(feature_id)
    
    # Nếu không tìm thấy Feature, trả về None
    if not feature:
        return None
    
    # Tạo dictionary chứa dữ liệu của Feature và FeatureType nếu có
    feature_data = {
        "id": feature.id,
        "description": feature.description,
        "feature_type": {
            "id": feature.feature_type.id,
            "name": feature.feature_type.name,
            "description": feature.feature_type.description,
        } if feature.feature_type else None,
    }
    
    return feature_data