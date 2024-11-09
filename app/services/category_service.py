from app.models.category import Category
from app.database import db

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
    return Category.query.get(category_id).to_dict() if Category.query.get(category_id) else None

def get_all_categories():
    return [category.to_dict() for category in Category.query.all()]

def update_category(category_id, category_data):
    category = Category.query.get(category_id)
    if category:
        category.name = category_data.get('name', category.name)
        category.description = category_data.get('description', category.description)
        category.min_lifespan = category_data.get('min_lifespan', category.min_lifespan)
        category.max_lifespan = category_data.get('max_lifespan', category.max_lifespan)
        category.default_salvage_value_rate = category_data.get('default_salvage_value_rate', category.default_salvage_value_rate)
        category.parent_id = category_data.get('parent_id', category.parent_id)
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

def filter_all_categories(page=1, per_page=10, min_lifespan=None, max_lifespan=None, 
                       name=None, description=None, default_salvage_value_rate=None, parent_id=None):
    query = Category.query

    # Áp dụng bộ lọc
    if min_lifespan is not None:
        query = query.filter(Category.min_lifespan >= min_lifespan)
    if max_lifespan is not None:
        query = query.filter(Category.max_lifespan <= max_lifespan)
    if name:
        query = query.filter(Category.name.ilike(f"%{name}%"))
    if default_salvage_value_rate is not None:
        query = query.filter(Category.default_salvage_value_rate == default_salvage_value_rate)
    if parent_id is not None:
        query = query.filter(Category.parent_id == parent_id)
    # Phân trang
    paginated_categories = query.paginate(page=page, per_page=per_page, error_out=False)
    categories = [category.to_dict() for category in paginated_categories.items]

    return {
        "categories": categories,
        "total": paginated_categories.total,
        "page": paginated_categories.page,
        "per_page": paginated_categories.per_page,
        "pages": paginated_categories.pages
    }
