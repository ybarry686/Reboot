"""
Methods for common queries in regards to the users
"""
from sqlalchemy import *
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
    if exists(s, Bookings, service_id=service_id):
        return None
    
    service = s.query(Services).filter(Services.id == service_id)[0]
    if service:
        booking = Bookings(user_id=user_id, service_id=service_id, start_time=start_time)    
        s.add(booking)
        s.commit()
        s.close()
        return booking
    s.close()
    return None

def cancel_booking(user_id, service_id, start_time): # not sure if start time is a necessary param, might have to differentiate between two bookings at the same place but differentt ime
    s = __init_session__()
    booking = get_elem(s, Bookings, user_id=user_id, service_id=service_id, start_time=start_time)
    if booking:
        booking.status = "Canceled" # I believe we just update status rather than remove the booking outright
        s.commit()

    s.close()

def get_bookings_for_user(user_id):
    s = __init_session__()
    l = get_elems(s, Bookings, user_id=user_id)
    s.close()
    return l # don't know if I have to not expose Query object


