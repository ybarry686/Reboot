from sqlalchemy import *
from sqlalchemy.orm.session import Session
from connection import *
from models import *
from favorite_queries import *
from user_queries import *
from search_queries import *
from datetime import datetime

'''
def print_user_table():
    s = init_session()
    users = s.query(Users).all()
    print(users)

def print_studio_table():
    s = init_session()
    studios = s.query(Studios).all()
    print(studios)

def print_services_table():
    s: Session = init_session()
    services = s.query(Services).all()
    print(services)
'''
def print_table(model):
    s: Session = init_session()
    rows = s.query(model).all()
    print(f"PRINTING {model.__name__} TABLE")
    for row in rows:
        print("\t" + str(row))
    print()

# seed.py

def seed_data():
    session = init_session()

    studio1 = Studios(
        name="Zen Float Studio",
        address="123 Main St, Austin, TX",
        lat=30.2672,
        lng=-97.7431,
        phone="512-555-0100",
        description="Float tank and infrared sauna recovery studio",
        category_tags="float,sauna"
    )

    studio2 = Studios(
        name="Recharge Sports Recovery",
        address="456 Congress Ave, Austin, TX",
        lat=30.2650,
        lng=-97.7440,
        phone="512-555-0101",
        description="Massage and cryotherapy for athletes",
        category_tags="massage,cryo"
    )

    session.add_all([studio1, studio2])
    session.commit()  # commit here so studio1.id and studio2.id get assigned

    service1 = Services(
        studio_id=studio1.id,
        name="60-Min Float Session",
        category="float",
        duration_min=60,
        price_cents=8000,
        description="Sensory deprivation float tank"
    )

    service2 = Services(
        studio_id=studio2.id,
        name="Deep Tissue Massage",
        category="massage",
        duration_min=45,
        price_cents=9500,
        description="Targeted deep tissue massage for muscle recovery"
    )

    session.add_all([service1, service2])
    
    user1 = Users(
        name="Zara Ike",
        email="zara@example.com",
        password_hash="hashed_pw_123"
    )

    session.add(user1)

    session.commit()
    session.close()

#seed_data()
add_booking(1, 2, datetime(2027, 8, 8, 20, 28, 35))
add_favorite(1, 1)

print_table(Users)
print_table(Studios)
print_table(Services)
print_table(Bookings)
print_table(Favorites)
