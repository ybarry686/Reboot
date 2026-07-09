from db.connection import session_scope
from db.models import Bookings, Services, Studios


def create_booking(user_id, service_id, start_time):
    with session_scope() as session:
        booking = Bookings(
            user_id=user_id, service_id=service_id, start_time=start_time, status="requested"
        )
        session.add(booking)
        session.flush()
        return booking.id


def list_bookings_for_user(user_id):
    with session_scope() as session:
        rows = (
            session.query(Bookings, Services, Studios)
            .join(Services, Services.id == Bookings.service_id)
            .join(Studios, Studios.id == Services.studio_id)
            .filter(Bookings.user_id == user_id)
            .order_by(Bookings.start_time.desc())
            .all()
        )
        return [
            {
                "id": b.id, "user_id": b.user_id, "service_id": b.service_id,
                "start_time": b.start_time, "status": b.status, "created_at": b.created_at,
                "service_name": svc.name, "duration_min": svc.duration_min, "price_cents": svc.price_cents,
                "studio_name": studio.name, "studio_address": studio.address, "studio_phone": studio.phone,
            }
            for b, svc, studio in rows
        ]


def get_booking_by_id(booking_id):
    with session_scope() as session:
        b = session.get(Bookings, booking_id)
        if not b:
            return None
        return {"id": b.id, "user_id": b.user_id, "service_id": b.service_id, "start_time": b.start_time, "status": b.status}


def cancel_booking(booking_id, user_id):
    with session_scope() as session:
        booking = (
            session.query(Bookings)
            .filter(Bookings.id == booking_id, Bookings.user_id == user_id)
            .first()
        )
        if not booking:
            return False
        booking.status = "cancelled"
        return True