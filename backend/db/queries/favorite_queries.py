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

def add_favorite(user_id, studio_id):
    s = __init_session__()
    s.add(Favorites(user_id, studio_id))
    s.commit()
    s.close()

def remove_favorite(user_id, studio_id):
    s = __init_session__()
    fav_to_delete = s.query(Favorites).filter(
        Favorites.user_id == user_id, Favorites.studio_id == studio_id) 
    if fav_to_delete:
        s.delete(fav_to_delete)
        s.commit()
    s.close()   

def get_favorites_for_user(user_id):
    s = __init_session__()
    #.query select all favorites, 
    favorites = s.query(Favorites).filter(Favorites.user_id == user_id)
    return favorites

