from db.connection import session_scope
from db.models import Services, Studios, service_to_dict, studio_to_dict


def search_studios(category=None, keyword=None):
    with session_scope() as session:
        query = session.query(Studios)
        if category:
            query = query.filter(Studios.category_tags.like(f"%{category}%"))
        if keyword:
            like = f"%{keyword}%"
            query = query.filter(
                (Studios.name.like(like))
                | (Studios.address.like(like))
                | (Studios.description.like(like))
            )
        rows = query.order_by(Studios.rating.desc()).all()
        return [studio_to_dict(s) for s in rows]


def get_studio_by_id(studio_id):
    with session_scope() as session:
        s = session.get(Studios, studio_id)
        return studio_to_dict(s) if s else None


def get_services_for_studio(studio_id):
    with session_scope() as session:
        rows = session.query(Services).filter(Services.studio_id == studio_id).all()
        return [service_to_dict(s) for s in rows]


def get_service_by_id(service_id):
    with session_scope() as session:
        s = session.get(Services, service_id)
        return service_to_dict(s) if s else None