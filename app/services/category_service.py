from app.models.category import Category
from app.models.asset import Asset
from app.models.asset_detail import AssetDetail
from app.database import db
from sqlalchemy import and_
from sqlalchemy.orm import aliased
from sqlalchemy import func
def create_category(category_data):
    category = Category(
        name=category_data['name'],
        description=category_data['description'],
        min_lifespan=category_data['min_lifespan'],
        max_lifespan=category_data['max_lifespan'],
        default_salvage_value_rate=category_data['default_salvage_value_rate'],
        parent_id=category_data.get('parent_id', None)
        
    )
    db.session.add(category)
    db.session.commit()
    return category.to_dict()

def get_category_by_id(category_id):
    ParentCategory = aliased(Category)  # Alias cho bảng cha
    result = Category.query.outerjoin(
        ParentCategory, Category.parent_id == ParentCategory.id
    ).with_entities(
        Category.id,
        Category.name,
        Category.description,
        Category.min_lifespan,
        Category.max_lifespan,
        Category.default_salvage_value_rate,
        Category.parent_id,
        Category.deleted_at,
        ParentCategory.name.label("parent_name")
    ).filter(Category.id == category_id).first()

    if result:
        return {
            "id": result.id,
            "name": result.name,
            "description": result.description,
            "min_lifespan": result.min_lifespan,
            "max_lifespan": result.max_lifespan,
            "default_salvage_value_rate": result.default_salvage_value_rate,
            "parent_id": result.parent_id,
            "parent_name": result.parent_name,
            "deleted_at": result.deleted_at
        }
    return None

def get_all_categories():
    ParentCategory = aliased(Category)
    results = Category.query.outerjoin(
        ParentCategory, Category.parent_id == ParentCategory.id
    ).with_entities(
        Category.id,
        Category.name,
        Category.description,
        Category.min_lifespan,
        Category.max_lifespan,
        Category.deleted_at,
        Category.default_salvage_value_rate,
        Category.parent_id,
        ParentCategory.name.label("parent_name")
    ).filter(Category.deleted_at.is_(None)).all()

    return [
        {
            "id": result.id,
            "name": result.name,
            "description": result.description,
            "min_lifespan": result.min_lifespan,
            "max_lifespan": result.max_lifespan,
            "default_salvage_value_rate": result.default_salvage_value_rate,
            "parent_id": result.parent_id,
            "parent_name": result.parent_name,
            "deleted_at": result.deleted_at
        }
        for result in results
    ]
def update_category(category_id, category_data):
    category = Category.query.get(category_id)
    if category:
        category.name = category_data.get('name', category.name)
        category.description = category_data.get('description', category.description)
        category.min_lifespan = category_data.get('min_lifespan', category.min_lifespan)
        category.max_lifespan = category_data.get('max_lifespan', category.max_lifespan)
        category.default_salvage_value_rate = category_data.get('default_salvage_value_rate', category.default_salvage_value_rate)
        category.parent_id = category_data.get('parent_id', category.parent_id)
        category.deleted_at = category_data.get('deleted_at', category.deleted_at)
        db.session.commit()
        return category.to_dict()
    return None

def delete_category(category_id):
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return True
    return False


def filter_all_categories(min_lifespan=None, max_lifespan=None, 
                          name=None, description=None, 
                          default_salvage_value_rate=None, parent_id=None):
    ParentCategory = aliased(Category)
    query = Category.query.outerjoin(ParentCategory, Category.parent_id == ParentCategory.id)
    query = query.filter(Category.deleted_at.is_(None))
    # Áp dụng các bộ lọc
    if min_lifespan is not None:
        query = query.filter(Category.min_lifespan >= min_lifespan)
    if max_lifespan is not None:
        query = query.filter(Category.max_lifespan <= max_lifespan)
    if name:
        query = query.filter(Category.name.ilike(f"%{name}%"))
    if description:
        query = query.filter(Category.description.ilike(f"%{description}%"))
    if default_salvage_value_rate is not None:
        epsilon = 1e-9  # Ngưỡng sai số nhỏ
        query = query.filter(and_(
            Category.default_salvage_value_rate >= default_salvage_value_rate - epsilon,
            Category.default_salvage_value_rate <= default_salvage_value_rate + epsilon
        ))
    if parent_id is not None:
        query = query.filter(Category.parent_id == parent_id)

    # Lấy danh sách kết quả với parent_name
    results = query.with_entities(
        Category.id,
        Category.name,
        Category.description,
        Category.deleted_at,
        Category.min_lifespan,
        Category.max_lifespan,
        Category.default_salvage_value_rate,
        Category.parent_id,
        ParentCategory.name.label("parent_name")
    ).all()

    return [
        {
            "id": result.id,
            "name": result.name,
            "description": result.description,
            "min_lifespan": result.min_lifespan,
            "max_lifespan": result.max_lifespan,
            "default_salvage_value_rate": result.default_salvage_value_rate,
            "parent_id": result.parent_id,
            "parent_name": result.parent_name,
            "deleted_at": result.deleted_at
        }
        for result in results
    ]

def get_all_buildings():
        # Lấy tất cả các tòa nhà từ bảng Category
        buildings = Category.query.all()
        return [
            {"id": building.id, "name": building.name, "description": building.description}
            for building in buildings
        ]
        
def get_category_statistics():
    """
    Lấy thống kê tài sản theo danh mục, trạng thái và số lượng đã bị xóa.
    """
    # Query để lấy tất cả danh mục
    categories_query = db.session.query(Category.name).all()
    categories = {category.name: {"statuses": {}, "deleted_count": 0} for category in categories_query}

    # Query để lấy thống kê tài sản theo danh mục và trạng thái
    statistics_query = (
        db.session.query(
            Category.name.label('category_name'),
            AssetDetail.status.label('status'),
            func.count(AssetDetail.id).label('count')
        )
        .join(Asset, Asset.id == AssetDetail.asset_id)
        .join(Category, Category.id == Asset.category_id)
        .filter(Asset.deleted_at.is_(None))  # Loại bỏ tài sản bị xóa khỏi thống kê chính
        .group_by(Category.name, AssetDetail.status)
    ).all()


    deleted_query = (
        db.session.query(
            Category.name.label('category_name'),
            func.count(Asset.id).label('deleted_count')
        )
        .join(Category, Category.id == Asset.category_id)
        .filter(Asset.deleted_at.isnot(None))  # Chỉ tính tài sản bị xóa
        .group_by(Category.name)
    ).all()

    # Xử lý dữ liệu từ query thống kê
    for row in statistics_query:
        category = categories.setdefault(row.category_name, {"statuses": {}, "deleted_count": 0})
        category["statuses"][row.status] = row.count

    # Xử lý dữ liệu từ query tài sản đã bị xóa
    for row in deleted_query:
        category = categories.setdefault(row.category_name, {"statuses": {}, "deleted_count": 0})
        category["deleted_count"] = row.deleted_count

    # Đảm bảo rằng mọi category đều có thông tin về tất cả các trạng thái và deleted_count
    for category in categories.values():
        if "deleted_count" not in category:
            category["deleted_count"] = 0  # Nếu không có tài sản bị xóa thì gán giá trị là 0
        # Đảm bảo rằng tất cả các trạng thái đều có giá trị mặc định là 0
        for status in ["available", "in_use", "maintainance"]:  # Đây là các trạng thái ví dụ, có thể tùy chỉnh
            if status not in category["statuses"]:
                category["statuses"][status] = 0

    return categories


def get_purchase_statistics(start_date, end_date):

    # Lấy tất cả danh mục
    categories_query = db.session.query(Category.name).all()
    categories = {category.name: {"total_items": 0, "total_amount": 0} for category in categories_query}

    # Truy vấn số sản phẩm đã mua và tổng tiền đã chi theo danh mục trong khoảng thời gian
    purchase_query = (
        db.session.query(
            Category.name.label('category_name'),
            func.count(AssetDetail.id).label('total_items'),  # Đếm số lượng tài sản đã mua
            func.sum(AssetDetail.purchase_price).label('total_amount')  # Tính tổng tiền đã chi
        )
        .join(Asset, Asset.id == AssetDetail.asset_id)
        .join(Category, Category.id == Asset.category_id)
        .filter(AssetDetail.purchase_date >= start_date, AssetDetail.purchase_date <= end_date)
        .group_by(Category.name)
    ).all()

    # Cập nhật kết quả vào dictionary categories
    for row in purchase_query:
        category = categories.setdefault(row.category_name, {"total_items": 0, "total_amount": 0})
        category["total_items"] = row.total_items
        category["total_amount"] = row.total_amount

    return categories