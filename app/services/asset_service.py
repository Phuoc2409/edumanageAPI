from app.models.asset import Asset
from app.database import db

def create_asset(asset_data):
    asset = Asset(
        asset_name=asset_data['asset_name'],
        description=asset_data['description'],
        category_id=asset_data['category_id']
    )
    db.session.add(asset)
    db.session.commit()
    return asset.to_dict()

def get_asset_by_id(asset_id):
    return Asset.query.get(asset_id).to_dict() if Asset.query.get(asset_id) else None

def get_all_assets():
    return [asset.to_dict() for asset in Asset.query.all()]

def update_asset(asset_id, asset_data):
    asset = Asset.query.get(asset_id)
    if asset:
        asset.asset_name = asset_data.get('asset_name', asset.asset_name)
        asset.description = asset_data.get('description', asset.description)
        asset.category_id = asset_data.get('category_id', asset.category_id)
        db.session.commit()
        return asset.to_dict()
    return None

def delete_asset(asset_id):
    asset = Asset.query.get(asset_id)
    if asset:
        db.session.delete(asset)
        db.session.commit()
        return True
    return False
