from app.models.asset_detail import AssetDetail
from app.models.asset import Asset
from app.models.category import Category
from app.database import db
import re
from datetime import datetime
from sqlalchemy import and_


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

def filter_asset_details(filters):
    # Bắt đầu query
    query = AssetDetail.query

    # Duyệt qua tất cả các trường trong filters và thêm điều kiện vào query
    for key, value in filters.items():
        if hasattr(AssetDetail, key) and value is not None:
            # Nếu giá trị là chuỗi, sử dụng LIKE để hỗ trợ tìm kiếm
            if isinstance(value, str):
                query = query.filter(getattr(AssetDetail, key).like(f"%{value}%"))
            else:
                # Các trường khác áp dụng bộ lọc chính xác
                query = query.filter(getattr(AssetDetail, key) == value)

    # Thực thi query và trả về tất cả thông tin của AssetDetail
    return [asset_detail.to_dict() for asset_detail in query.all()]

from sqlalchemy.orm import joinedload

def filter_asset_details_by_room_floor_building(filters):
   # Các tham số lọc
    room_number = filters.get("room_number")
    floor_id = filters.get("floor_id")
    building_id = filters.get("building_id")

    # Bắt đầu query chính
    query = db.session.query(AssetDetail)

    # Lọc theo mã phòng
    if room_number:
        # Tìm asset_detail đại diện cho phòng với mã room_number
        room_asset_detail = db.session.query(AssetDetail.id).filter_by(identifier_number=room_number).first()
        if not room_asset_detail:
            raise Exception(f"No asset detail found with room_number = {room_number}")

        query = query.filter(AssetDetail.parent_id == room_asset_detail.id)

    # Lọc theo tầng
    if floor_id:
        # Tìm các phòng thuộc tầng
        subquery_rooms = (
            db.session.query(AssetDetail.id)
            .filter(AssetDetail.asset_id == floor_id)
            .subquery()
        )
        query = query.filter(AssetDetail.parent_id.in_(subquery_rooms))

    # Lọc theo tòa nhà
    if building_id:
        # Tìm các tầng thuộc tòa nhà
        subquery_floors = (
            db.session.query(Asset.id)
            .filter(Asset.category_id == building_id)
            .subquery()
        )
        # Tìm các phòng thuộc các tầng trong tòa nhà
        subquery_rooms = (
            db.session.query(AssetDetail.id)
            .filter(AssetDetail.asset_id.in_(subquery_floors))
            .subquery()
        )
        query = query.filter(AssetDetail.parent_id.in_(subquery_rooms))

    # Thực thi query và trả về kết quả
    filtered_results = query.all()
    return [
        {
            "id": detail.id,
            "asset_name": detail.asset.asset_name,
            "identifier_number": detail.identifier_number,
            "parent_id": detail.parent_id,
            "status": detail.status,
            "purchase_date": detail.purchase_date,
            "last_maintenance_date": detail.last_maintenance_date,
        }
        for detail in filtered_results
    ]

def filter_by_floor_and_room(filters):
    # Lấy các tham số lọc từ body request
    floor_id = filters.get("floor_id")
    room_number = filters.get("room_number")

    # Bắt đầu query
    query = AssetDetail.query

    # Lọc theo floor_id (ID tầng)
    if floor_id:
        query = query.filter_by(parent_id=floor_id)

    # Lọc theo room_number (số phòng)
    if room_number:
        query = query.filter_by(identifier_number=room_number)

    # Trả về kết quả
    return [asset_detail.to_dict() for asset_detail in query.all()]

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