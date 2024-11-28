from app.models.requirement_detail import RequirementDetail
from app.database import db

def create_requirement_detail(requirement_detail_data):
    requirement_detail = RequirementDetail(
        asset_detail_id=requirement_detail_data['asset_detail_id'],
        requirement_type=requirement_detail_data['requirement_type'],
        description=requirement_detail_data['description']
    )
    db.session.add(requirement_detail)
    db.session.commit()
    return requirement_detail.to_dict()

def get_requirement_detail_by_id(requirement_detail_id):
    return RequirementDetail.query.get(requirement_detail_id).to_dict() if RequirementDetail.query.get(requirement_detail_id) else None

def get_all_requirement_details():
    return [requirement_detail.to_dict() for requirement_detail in RequirementDetail.query.all()]

def update_requirement_detail(requirement_detail_id, requirement_detail_data):
    requirement_detail = RequirementDetail.query.get(requirement_detail_id)
    if requirement_detail:
        requirement_detail.asset_detail_id = requirement_detail_data.get('asset_detail_id', requirement_detail.asset_detail_id)
        requirement_detail.requirement_type = requirement_detail_data.get('requirement_type', requirement_detail.requirement_type)
        requirement_detail.description = requirement_detail_data.get('description', requirement_detail.description)
        requirement_detail.deleted_at = requirement_detail_data.get('deleted_at', requirement_detail.deleted_at)
        db.session.commit()
        return requirement_detail.to_dict()
    return None

def delete_requirement_detail(requirement_detail_id):
    requirement_detail = RequirementDetail.query.get(requirement_detail_id)
    if requirement_detail:
        db.session.delete(requirement_detail)
        db.session.commit()
        return True
    return False
