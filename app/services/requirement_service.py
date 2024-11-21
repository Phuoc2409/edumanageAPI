from ..database import db
from ..models.requirement import Requirement


def create_requirement(data):
    """
    Tạo yêu cầu mới.
    """
    new_requirement = Requirement(
        user_id=data.get("user_id"),
        date=data.get("date"),
        description=data.get("description"),
        status=data.get("status")
    )
    db.session.add(new_requirement)
    db.session.commit()
    return new_requirement.to_dict()


def get_all_requirements():
    """
    Lấy danh sách tất cả các yêu cầu.
    """
    requirements = Requirement.query.all()
    return [req.to_dict() for req in requirements]


def get_requirement_by_id(requirement_id):
    """
    Lấy thông tin yêu cầu theo ID.
    """
    requirement = Requirement.query.get(requirement_id)
    if requirement:
        return requirement.to_dict()
    return None


def update_requirement(requirement_id, data):
    """
    Cập nhật thông tin yêu cầu.
    """
    requirement = Requirement.query.get(requirement_id)
    if not requirement:
        return None

    requirement.user_id = data.get("user_id", requirement.user_id)
    requirement.date = data.get("date", requirement.date)
    requirement.description = data.get("description", requirement.description)
    requirement.status = data.get("status", requirement.status)

    db.session.commit()
    return requirement.to_dict()


def delete_requirement(requirement_id):
    """
    Xóa một yêu cầu.
    """
    requirement = Requirement.query.get(requirement_id)
    if not requirement:
        return False

    db.session.delete(requirement)
    db.session.commit()
    return True
