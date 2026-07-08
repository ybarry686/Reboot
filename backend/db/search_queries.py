"""
Methods for common queries in regards to database search
"""

from sqlalchemy import *
from connection import *
from models import *


def search_studios(keyword):
    s = init_session()
    return search(s, Studios, keyword, ["name", "address", "description", "category_tags"])

def search_services(keyword):
    s = init_session()
    return search(s, Services, keyword, ["name", "category", "description"])