from app.models.feature_type import FeatureType
from app.database import db

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
