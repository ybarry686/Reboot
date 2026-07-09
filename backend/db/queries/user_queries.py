from db.connection import session_scope
from db.models import Users, user_to_dict


def get_user_by_email(email):
    with session_scope() as session:
        user = session.query(Users).filter(Users.email == email).first()
        return user_to_dict(user) if user else None


def get_user_by_id(user_id):
    with session_scope() as session:
        user = session.get(Users, user_id)
        return user_to_dict(user) if user else None


def create_user(name, email, password_hash):
    with session_scope() as session:
        user = Users(name=name, email=email, password_hash=password_hash)
        session.add(user)
        session.flush()
        return user.id


def update_user(user_id, name, email):
    with session_scope() as session:
        user = session.get(Users, user_id)
        user.name = name
        user.email = email