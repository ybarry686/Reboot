from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from services.user_client import get_profile, update_profile, UserUpdateError
from utils.decorators import login_required

bp = Blueprint("user", __name__, url_prefix="/profile")


@bp.route("/", methods=["GET", "POST"])
@login_required
def profile():
    user_id = session["user_id"]
    if request.method == "POST":
        try:
            user = update_profile(
                user_id, request.form["name"].strip(), request.form["email"].strip().lower()
            )
            session["user_name"] = user["name"]
            flash("Profile updated.", "success")
        except UserUpdateError as exc:
            flash(str(exc), "error")
            return redirect(url_for("user.profile"))
    user = get_profile(user_id)
    return render_template("profile.html", user=user)