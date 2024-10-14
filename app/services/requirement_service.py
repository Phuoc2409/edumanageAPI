from app.models.requirement import Requirement
from app.database import db

def create_requirement(requirement_data):
    requirement = Requirement(
        user_id=requirement_data['user_id'],
        requester_identifier=requirement_data['requester_identifier'],
        date=requirement_data['date'],
        description=requirement_data['description'],
        status=requirement_data['status']
    )
    db.session.add(requirement)
    db.session.commit()
    return requirement.to_dict()

def get_requirement_by_id(requirement_id):
    return Requirement.query.get(requirement_id).to_dict() if Requirement.query.get(requirement_id) else None

def get_all_requirements():
    return [requirement.to_dict() for requirement in Requirement.query.all()]

def update_requirement(requirement_id, requirement_data):
    requirement = Requirement.query.get(requirement_id)
    if requirement:
        requirement.user_id = requirement_data.get('user_id', requirement.user_id)
        requirement.requester_identifier = requirement_data.get('requester_identifier', requirement.requester_identifier)
        requirement.date = requirement_data.get('date', requirement.date)
        requirement.description = requirement_data.get('description', requirement.description)
        requirement.status = requirement_data.get('status', requirement.status)
        db.session.commit()
        return requirement.to_dict()
    return None

def delete_requirement(requirement_id):
    requirement = Requirement.query.get(requirement_id)
    if requirement:
        db.session.delete(requirement)
        db.session.commit()
        return True
    return False
