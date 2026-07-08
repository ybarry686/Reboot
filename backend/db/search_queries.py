"""
Methods for common queries in regards to database search
"""

from sqlalchemy import *
from connection import *
from models import *


def search_services(keyword):
    s = init_session()
    all_services = get_elems(s, Services)
    res = []
    for service in all_services:
        if keyword in service:
            res.append(service)
    
    return res