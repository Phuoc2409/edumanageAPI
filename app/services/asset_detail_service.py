from app.models.asset_detail import AssetDetail
from app.database import db

def create_asset_detail(asset_detail_data):
    asset_detail = AssetDetail(
        identifier_number=asset_detail_data['identifier_number'],
        user_id=asset_detail_data['user_id'],
        purchase_date=asset_detail_data['purchase_date'],
        purchase_price=asset_detail_data['purchase_price'],
        used_years=asset_detail_data['used_years'],
        last_maintenance_date=asset_detail_data['last_maintenance_date'],
        status=asset_detail_data['status']
    )
    db.session.add(asset_detail)
    db.session.commit()
    return asset_detail.to_dict()

def get_asset_detail_by_id(asset_detail_id):
    return AssetDetail.query.get(asset_detail_id).to_dict() if AssetDetail.query.get(asset_detail_id) else None

def get_all_asset_details():
    return [asset_detail.to_dict() for asset_detail in AssetDetail.query.all()]

def update_asset_detail(asset_detail_id, asset_detail_data):
    asset_detail = AssetDetail.query.get(asset_detail_id)
    if asset_detail:
        asset_detail.identifier_number = asset_detail_data.get('identifier_number', asset_detail.identifier_number)
        asset_detail.user_id = asset_detail_data.get('user_id', asset_detail.user_id)
        asset_detail.purchase_date = asset_detail_data.get('purchase_date', asset_detail.purchase_date)
        asset_detail.purchase_price = asset_detail_data.get('purchase_price', asset_detail.purchase_price)
        asset_detail.used_years = asset_detail_data.get('used_years', asset_detail.used_years)
        asset_detail.last_maintenance_date = asset_detail_data.get('last_maintenance_date', asset_detail.last_maintenance_date)
        asset_detail.status = asset_detail_data.get('status', asset_detail.status)
        db.session.commit()
        return asset_detail.to_dict()
    return None

def delete_asset_detail(asset_detail_id):
    asset_detail = AssetDetail.query.get(asset_detail_id)
    if asset_detail:
        db.session.delete(asset_detail)
        db.session.commit()
        return True
    return False
