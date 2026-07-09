from db.connection import session_scope
from db.models import Favorites, Studios, studio_to_dict


def list_favorites_for_user(user_id):
    with session_scope() as session:
        rows = (
            session.query(Studios)
            .join(Favorites, Favorites.studio_id == Studios.id)
            .filter(Favorites.user_id == user_id)
            .order_by(Favorites.created_at.desc())
            .all()
        )
        return [studio_to_dict(s) for s in rows]


def is_favorited(user_id, studio_id):
    with session_scope() as session:
        exists = (
            session.query(Favorites)
            .filter(Favorites.user_id == user_id, Favorites.studio_id == studio_id)
            .first()
        )
        return exists is not None


def add_favorite(user_id, studio_id):
    with session_scope() as session:
        exists = (
            session.query(Favorites)
            .filter(Favorites.user_id == user_id, Favorites.studio_id == studio_id)
            .first()
        )
        if not exists:
            session.add(Favorites(user_id=user_id, studio_id=studio_id))


def remove_favorite(user_id, studio_id):
    with session_scope() as session:
        session.query(Favorites).filter(
            Favorites.user_id == user_id, Favorites.studio_id == studio_id
        ).delete()