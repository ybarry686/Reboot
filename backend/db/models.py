from sqlalchemy import Column, Float, ForeignKey, Integer, String, TIMESTAMP, UniqueConstraint, func

from db.connection import Base, engine


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Studios(Base):
    __tablename__ = "studios"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    lat = Column(Float)
    lng = Column(Float)
    phone = Column(String)
    description = Column(String)
    category_tags = Column(String, nullable=False)
    rating = Column(Float)
    source = Column(String, default="manual")
    source_place_id = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Services(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    studio_id = Column(Integer, ForeignKey("studios.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    category_tags = Column(String, nullable=False)
    duration_min = Column(Integer, nullable=False)
    price_cents = Column(Integer, nullable=False)
    description = Column(String)


class Bookings(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    status = Column(String, default="requested")
    created_at = Column(TIMESTAMP, server_default=func.now())


class Favorites(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "studio_id"),)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    studio_id = Column(Integer, ForeignKey("studios.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


def init_db():
    Base.metadata.create_all(engine)


def studio_to_dict(s):
    return {
        "id": s.id, "name": s.name, "address": s.address, "lat": s.lat, "lng": s.lng,
        "phone": s.phone, "description": s.description, "category_tags": s.category_tags,
        "rating": s.rating, "source": s.source, "source_place_id": s.source_place_id,
        "created_at": s.created_at,
    }


def service_to_dict(s):
    return {
        "id": s.id, "studio_id": s.studio_id, "name": s.name, "category": s.category_tags,
        "duration_min": s.duration_min, "price_cents": s.price_cents, "description": s.description,
    }


def user_to_dict(u):
    return {
        "id": u.id, "name": u.name, "email": u.email,
        "password_hash": u.password_hash, "created_at": u.created_at,
    }