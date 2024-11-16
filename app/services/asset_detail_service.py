from app.models.asset_detail import AssetDetail
from app.models.asset import Asset
from app.models.category import Category
from app.database import db
import re
from datetime import datetime


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
def get_all_asset_detail(asset_detail_id):
        # Tìm AssetDetail theo ID
        asset_detail = AssetDetail.query.get_or_404(asset_detail_id)

        # Lấy danh sách đặc trưng liên quan
        features = [
            {
                "feature_id": af.feature.id,
                "feature_description": af.feature.description,
                "feature_type": af.feature.feature_type.name if af.feature.feature_type else None,
                "asset_feature_description": af.description
            }
            for af in asset_detail.features
        ]

        # Tạo dictionary chứa dữ liệu chi tiết
        data = {
            "id": asset_detail.id,
            "asset": asset_detail.asset.to_dict() if asset_detail.asset else None,
            "identifier_number": asset_detail.identifier_number,
            "user": asset_detail.user.to_dict() if asset_detail.user else None,
            "purchase_date": asset_detail.purchase_date,
            "purchase_price": asset_detail.purchase_price,
            "used_years": asset_detail.used_years,
            "last_maintenance_date": asset_detail.last_maintenance_date,
            "parent": asset_detail.parent.to_dict() if asset_detail.parent else None,
            "status": asset_detail.status,
            "features": features
        }

        return data

def get_rooms_by_floor(floor_id):
    rooms = AssetDetail.query.filter_by(asset_id=floor_id).all()
    return [
        {
            "id": room.id,
            "identifier_number": room.identifier_number,
            "purchase_date": room.purchase_date.strftime('%Y-%m-%d') if isinstance(room.purchase_date, datetime) else room.purchase_date,
            "purchase_price": room.purchase_price,
            "used_years": room.used_years,
            "last_maintenance_date": room.last_maintenance_date.strftime('%Y-%m-%d') if isinstance(room.last_maintenance_date, datetime) else room.last_maintenance_date,
            "status": room.status
        }
        for room in rooms
    ]