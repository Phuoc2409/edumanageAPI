from app.models.feature import Feature
from app.database import db
from app.models.feature_type import FeatureType

def create_feature(feature_data):
    feature = Feature(
        feature_type_id=feature_data['feature_type_id'],
        description=feature_data['description']
    )
    db.session.add(feature)
    db.session.commit()
    return feature.to_dict()

def get_feature_by_id(feature_id):
    return Feature.query.get(feature_id).to_dict() if Feature.query.get(feature_id) else None

def get_all_features():
    return [feature.to_dict() for feature in Feature.query.all()]

def update_feature(feature_id, feature_data):
    feature = Feature.query.get(feature_id)
    if feature:
        feature.feature_type_id = feature_data.get('feature_type_id', feature.feature_type_id)
        feature.description = feature_data.get('description', feature.description)
        feature.deleted_at = feature_data.get('deleted_at', feature.deleted_at)
        db.session.commit()
        return feature.to_dict()
    return None

def delete_feature(feature_id):
    feature = Feature.query.get(feature_id)
    if feature:
        db.session.delete(feature)
        db.session.commit()
        return True
    return False


def filter_all_features(description=None, feature_type_id=None,feature_type_name=None):
    query = Feature.query.join(FeatureType)

    # Áp dụng bộ lọc
    if description:
        query = query.filter(Feature.description.ilike(f"%{description}%"))
    if feature_type_id is not None:
        query = query.filter(Feature.feature_type_id == feature_type_id)
    if feature_type_name:
        query = query.filter(FeatureType.name.ilike(f"%{feature_type_name}%"))


    # Trả về danh sách tất cả các tính năng phù hợp với bộ lọc
    return [feature.to_dict() for feature in query.all()]


