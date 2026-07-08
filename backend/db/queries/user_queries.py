"""
Methods for common queries in regards to the users
"""
from sqlalchemy import *
from connection import __init_session__
from connection import *
from models import *

# add user
# get user data (name, email, password(?))
# get user bookings
def __init_session__() -> Session:
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

# users:


# bookings: create, list, cancel
def add_booking(user_id, service_id, start_time):
    # am not sure where start_time would go now that I think about it, does the user pick the service times?
    # skip the above process for now, let user choose freely
    s = __init_session__()
    service = s.query(Services).filter(Services.id == service_id)[0]
    if service:
        booking = Bookings(user_id=user_id, service_id=service_id, start_time=start_time)    
        s.add(booking)
        s.commit()
    
    return booking

