from sqlalchemy import *
from sqlalchemy.orm.session import Session
from connection import *

class ReprMixin:
    '''
    class that allows for inheritors to have same string representation
    '''

    def __repr__(self):
        values = {} # colums->value mapping 
        for c in self.__table__.columns:
            key = c.name # column name
            value = getattr(self, c.name) # value of column
            values[key] = value

        return f"<{self.__class__.__name__} {values}>"

class Users(Base, ReprMixin):
    __tablename__ = 'users'
    id: Column[int] = Column(Integer, primary_key=True)
    name: Column[str] = Column(String)
    email: Column[str] = Column(String)
    password_hash = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Studios(Base, ReprMixin):
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

class Services(Base, ReprMixin):
    __tablename__ = 'services'
    id: Column[int] = Column(Integer, primary_key=True)
    studio_id = Column(Integer, ForeignKey(Studios.id))
    name: Column[str] = Column(String)
    category: Column[str] = Column(String)
    duration_min = Column(Integer)
    price_cents = Column(Integer)
    description: Column[str] = Column(String)

class Bookings(Base, ReprMixin):
    __tablename__ = 'bookings'
    id: Column[int] = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(Users.id))
    service_id = Column(Integer, ForeignKey(Services.id))
    start_time = Column(TIMESTAMP)
    status = Column(String, default="Confirmed") # cancelled, active(?)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Favorites(Base, ReprMixin):
    __tablename__ = 'favorites'
    id: Column[int] = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(Users.id))
    studio_id = Column(Integer, ForeignKey(Studios.id))

Base.metadata.create_all(engine)
SessionObj = sessionmaker(bind=engine)

def init_session() -> Session:
    session = SessionObj()
    return session

def get_elem(session, model, **kwargs):
    return session.query(model).filter_by(**kwargs).first()

def get_elems(session, model, **kwargs):
    return session.query(model).filter_by(**kwargs)

def exists(session, model, **kwargs):
    return get_elem(session, model, **kwargs) is not None

def search(session, model, keyword, fields):
    keyword = keyword.lower()
    res = []

    all_models = get_elems(session, model)
    
    for row in all_models: # each elem
        for field in fields:
            value = getattr(row, field) # because we can't do row.field
            if value and keyword in value.lower():
                res.append(row) # append this elem
                break # don't have to search the rest since we already know this elem is valid
    
    return res
