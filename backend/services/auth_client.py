from werkzeug.security import generate_password_hash, check_password_hash

from db.queries.user_queries import create_user, get_user_by_email


class AuthError(Exception):
    pass


def signup(name, email, password):
    if get_user_by_email(email):
        raise AuthError("An account with that email already exists.")
    if len(password) < 8:
        raise AuthError("Password must be at least 8 characters.")
    password_hash = generate_password_hash(password)
    return create_user(name, email, password_hash)


def login(email, password):
    user = get_user_by_email(email)
    if not user or not check_password_hash(user["password_hash"], password):
        raise AuthError("Incorrect email or password.")
    return user