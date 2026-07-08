"""
Methods for common queries in regards to the favorites list
"""
from sqlalchemy import *
from connection import *
from models import *

# add favorite
# remove favorite
# get favorite

def add_favorite(user_id, studio_id):
    s = init_session()
    if not exists(s, Favorites, user_id=user_id, studio_id=studio_id):
        s.add(Favorites(user_id=user_id, studio_id=studio_id))
        s.commit()
    s.close()

def remove_favorite(user_id, studio_id):
    s = init_session()
    fav_to_delete = s.query(Favorites).filter(
        Favorites.user_id == user_id, Favorites.studio_id == studio_id).first()
    if fav_to_delete:
        s.delete(fav_to_delete)
        s.commit()
    s.close()   

def get_favorites_for_user(user_id):
    s = init_session()
    #.query select all favorites, 
    favorites = s.query(Favorites).filter(Favorites.user_id == user_id)
    s.close()
    return favorites

