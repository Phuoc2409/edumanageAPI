from app.models.category import Category
from app.database import db
from sqlalchemy import and_
from sqlalchemy.orm import aliased
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
            "parent_name": result.parent_name
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