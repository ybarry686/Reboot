from db.queries.user_queries import get_user_by_id, update_user, get_user_by_email


class UserUpdateError(Exception):
    pass


def get_profile(user_id):
    return get_user_by_id(user_id)


def update_profile(user_id, name, email):
    existing = get_user_by_email(email)
    if existing and existing["id"] != user_id:
        raise UserUpdateError("That email is already in use by another account.")
    update_user(user_id, name, email)
    return get_user_by_id(user_id)