from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from db.queries.search_queries import get_studio_by_id, get_services_for_studio
from db.queries.favorite_queries import is_favorited
from db.queries.booking_queries import list_bookings_for_user
from services.booking_client import book_service, cancel, BookingError
from utils.decorators import login_required

bp = Blueprint("booking", __name__)


@bp.route("/studios/<int:studio_id>")
def studio_detail(studio_id):
    studio = get_studio_by_id(studio_id)
    if not studio:
        flash("Studio not found.", "error")
        return redirect(url_for("search.home"))
    services = get_services_for_studio(studio_id)
    favorited = bool(session.get("user_id")) and is_favorited(session["user_id"], studio_id)
    return render_template("studio_detail.html", studio=studio, services=services, favorited=favorited)


@bp.route("/bookings", methods=["POST"])
@login_required
def create():
    studio_id = request.form["studio_id"]
    try:
        book_service(session["user_id"], int(request.form["service_id"]), request.form["start_time"])
        studio = get_studio_by_id(int(studio_id))
        if studio and studio.get("phone"):
            flash(f"Request sent! Call {studio['name']} at {studio['phone']} to confirm your appointment.", "success")
        else:
            flash(f"Request sent! Contact {studio['name'] if studio else 'the studio'} directly to confirm your appointment.", "success")
    except BookingError as exc:
        flash(str(exc), "error")
    return redirect(url_for("booking.studio_detail", studio_id=studio_id))


@bp.route("/bookings/mine")
@login_required
def mine():
    bookings = list_bookings_for_user(session["user_id"])
    return render_template("my_bookings.html", bookings=bookings)


@bp.route("/bookings/<int:booking_id>/cancel", methods=["POST"])
@login_required
def cancel_view(booking_id):
    try:
        cancel(session["user_id"], booking_id)
        flash("Booking cancelled.", "success")
    except BookingError as exc:
        flash(str(exc), "error")
    return redirect(url_for("booking.mine"))