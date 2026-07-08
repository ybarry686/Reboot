from sqlalchemy import *
from sqlalchemy.orm.session import Session
from connection import *

class Users(Base):
    __tablename__ = 'users'
    id: Column[int] = Column(Integer, primary_key=True)
    name: Column[str] = Column(String)
    email: Column[str] = Column(String)
    password_hash = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Studios(Base):
    __tablename__ = 'studios'
    id: Column[int] = Column(Integer, primary_key=True)
    name: Column[str] = Column(String)
    address: Column[str] = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    phone: Column[str] = Column(String)
    description: Column[str] = Column(String)
    source_place_id: Column[str] = Column(String)
    category_tags: Column[str] = Column(String) # each tag separated by comma
    created_at = Column(TIMESTAMP, server_default=func.now())

class Services(Base):
    __tablename__ = 'services'
    id: Column[int] = Column(Integer, primary_key=True)
    studio_id = Column(Integer, ForeignKey(Studios.id))
    name: Column[str] = Column(String)
    category_tags: Column[str] = Column(String)
    duration_min = Column(Integer)
    price_cents = Column(Integer)
    description: Column[str] = Column(String)

class Bookings(Base):
    ___tablename__ = 'bookings'
    id: Column[int] = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(Users.id))
    service_id = Column(Integer, ForeignKey(Services.id))
    start_time = Column(TIMESTAMP)
    status = Column(String, default="Confirmed") # cancelled, active(?)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Favorites(Base):
    __tablename__ = 'favorites'
    id: Column[int] = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(Users.id))
    studio_id = Column(Integer, ForeignKey(Studios.id))

Base.metadata.create_all(engine)

def __init_session__() -> Session:
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


