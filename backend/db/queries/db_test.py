from sqlalchemy import *
from backend.db.connection import __init_session__
from backend.db.connection import *
from backend.db.models import *
from favorite_queries import *
from user_queries import *
from search_queries import *


def print_user_table():
    s = __init_session__()
    users = s.query(Users).add()
    print(users)

print_user_table()