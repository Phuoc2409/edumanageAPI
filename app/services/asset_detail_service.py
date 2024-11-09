from app.models.asset_detail import AssetDetail
from app.models.asset import Asset
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

def search_asset_details(filters):
    # Bắt đầu truy vấn từ bảng AssetDetail và kết hợp với bảng Asset
    query = db.session.query(AssetDetail).join(Asset)

    # Áp dụng các bộ lọc dựa trên các giá trị đầu vào
    if "identifier_number" in filters:
        query = query.filter(AssetDetail.identifier_number == filters["identifier_number"])
    if "user_id" in filters:
        query = query.filter(AssetDetail.user_id == filters["user_id"])

    # Tìm kiếm theo khoảng ngày tháng
    if "start_date" in filters and "end_date" in filters:
        query = query.filter(AssetDetail.purchase_date.between(filters["start_date"], filters["end_date"]))
    elif "start_date" in filters:
        query = query.filter(AssetDetail.purchase_date >= filters["start_date"])
    elif "end_date" in filters:
        query = query.filter(AssetDetail.purchase_date <= filters["end_date"])

    # Tìm kiếm theo khoảng giá cả
    if "min_price" in filters and "max_price" in filters:
        query = query.filter(AssetDetail.purchase_price.between(filters["min_price"], filters["max_price"]))
    elif "min_price" in filters:
        query = query.filter(AssetDetail.purchase_price >= filters["min_price"])
    elif "max_price" in filters:
        query = query.filter(AssetDetail.purchase_price <= filters["max_price"])

    if "status" in filters:
        query = query.filter(AssetDetail.status == filters["status"])

    # Tìm kiếm theo category_id từ bảng Asset
    if "category_id" in filters:
        query = query.filter(Asset.category_id == filters["category_id"])

    # Tìm kiếm theo asset_id từ bảng AssetDetail
    if "asset_id" in filters:
        query = query.filter(AssetDetail.asset_id == filters["asset_id"])

    return [asset_detail.to_dict() for asset_detail in query.all()]