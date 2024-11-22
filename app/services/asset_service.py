from app.models.asset import Asset
from app.models.category import Category
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
        asset.deleted_at = asset_data.get('deleted_at', asset.deleted_at)
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
def get_floors_by_building(building_id):
        # Lấy các tầng của một tòa nhà từ bảng Asset
        building = Category.query.get(building_id)
        if not building:
            return None  # Nếu không tìm thấy tòa nhà

        floors = Asset.query.filter_by(category_id=building_id).all()
        return [
            {"id": floor.id, "asset_name": floor.asset_name, "description": floor.description,"deleted_at":floor.deleted_at}
            for floor in floors
        ]
def filter_assets(filters):
    """
    Lọc và tìm kiếm trên bảng Asset dựa theo các trường và giá trị trong filters.
    """
    query = Asset.query

    # Duyệt qua tất cả các trường trong filters và thêm điều kiện vào query
    for key, value in filters.items():
        if hasattr(Asset, key) and value is not None:
            # Nếu giá trị là chuỗi, sử dụng LIKE để hỗ trợ tìm kiếm
            if isinstance(value, str):
                query = query.filter(getattr(Asset, key).like(f"%{value}%"))
            else:
                # Các trường khác áp dụng bộ lọc chính xác
                query = query.filter(getattr(Asset, key) == value)

    # Thực thi query và trả về tất cả thông tin của Asset
    return [asset.to_dict() for asset in query.all()]
