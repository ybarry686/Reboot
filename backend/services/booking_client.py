from datetime import datetime

from db.queries.booking_queries import create_booking, cancel_booking
from db.queries.search_queries import get_service_by_id


class BookingError(Exception):
    pass


def book_service(user_id, service_id, start_time):
    service = get_service_by_id(service_id)
    if not service:
        raise BookingError("That service no longer exists.")
    if not start_time:
        raise BookingError("Pick a date and time for your appointment.")
    try:
        start_dt = datetime.fromisoformat(start_time)
    except ValueError:
        raise BookingError("That date/time doesn't look right -- please pick it again.")
    return create_booking(user_id, service_id, start_dt)


def cancel(user_id, booking_id):
    ok = cancel_booking(booking_id, user_id)
    if not ok:
        raise BookingError("Booking not found, or it isn't yours to cancel.")