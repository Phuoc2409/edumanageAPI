from app.models.asset_feature import AssetFeature
from app.database import db

def create_asset_feature(asset_feature_data):
    asset_feature = AssetFeature(
        asset_feature_name=asset_feature_data['asset_feature_name'],
        description=asset_feature_data['description'],
        asset_detail_id=asset_feature_data['asset_detail_id'],
        feature_id=asset_feature_data['feature_id'],
    )
    db.session.add(asset_feature)
    db.session.commit()
    return asset_feature.to_dict()

def get_asset_feature_by_id(asset_feature_id):
    return AssetFeature.query.get(asset_feature_id).to_dict() if AssetFeature.query.get(asset_feature_id) else None

def get_all_asset_features():
    return [asset_feature.to_dict() for asset_feature in AssetFeature.query.all()]

def update_asset_feature(asset_feature_id, asset_feature_data):
    asset_feature = AssetFeature.query.get(asset_feature_id)
    if asset_feature:
        asset_feature.asset_feature_name = asset_feature_data.get('asset_feature_name', asset_feature.asset_feature_name)
        asset_feature.description = asset_feature_data.get('description', asset_feature.description)
        asset_feature.description = asset_feature_data.get('asset_detail_id', asset_feature.asset_detail_id)
        asset_feature.description = asset_feature_data.get('feature_id', asset_feature.feature_id)
        db.session.commit()
        return asset_feature.to_dict()
    return None

def delete_asset_feature(asset_feature_id):
    asset_feature = AssetFeature.query.get(asset_feature_id)
    if asset_feature:
        db.session.delete(asset_feature)
        db.session.commit()
        return True
    return False
