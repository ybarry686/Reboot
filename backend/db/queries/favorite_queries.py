"""
Methods for common queries in regards to the favorites list
"""
from sqlalchemy import *
from connection import *

# add favorite
# remove favorite
# get favorite

def __init_session__():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def add_favorite():
    pass

def get_favorites_for_user(user_id):
    s = __init_session__()
    #.query select all favorites, 
    favorites = s.query(Favorites).filter(Favorites.user_id == user_id)
    return Favorites