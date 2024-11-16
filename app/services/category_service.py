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
def get_all_buildings():
    buildings = Category.query.filter_by(parent_id=0).all()
    return [
        {
            "id": building.id,
            "name": building.name,
            "description": building.description,
            "min_lifespan": building.min_lifespan,
            "max_lifespan": building.max_lifespan,
            "default_salvage_value_rate": building.default_salvage_value_rate
        }
        for building in buildings
    ]