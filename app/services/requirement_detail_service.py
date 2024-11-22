from app.models.requirement_detail import RequirementDetail
from app.database import db
from app.models.requirement import Requirement
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


def get_specific_requirement_detail(requirement_id):
    # Tìm Requirement theo ID
    requirement = Requirement.query.get(requirement_id)
    if not requirement:
        return None

    # Lấy các chi tiết yêu cầu liên quan từ RequirementDetail
    requirement_details = [
        {
            "detail_id": detail.id,
            "asset_detail_id": detail.asset_detail_id,
            "requirement_type": detail.requirement_type,
            "description": detail.description
        }
        for detail in requirement.requirement_details  # Giả sử có quan hệ với RequirementDetail
    ]

    # Chuẩn bị dữ liệu chi tiết yêu cầu
    data = {
        "id": requirement.id,
        "user_id": requirement.user_id,
        "date": requirement.date.isoformat(),
        "description": requirement.description,
        "status": requirement.status,
        "requirement_details": requirement_details
    }

    return data