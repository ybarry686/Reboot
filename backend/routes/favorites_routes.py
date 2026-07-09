from flask import Blueprint, render_template, redirect, url_for, session, request

from db.queries.favorite_queries import list_favorites_for_user, is_favorited, add_favorite, remove_favorite
from utils.decorators import login_required

bp = Blueprint("favorites", __name__, url_prefix="/favorites")


@bp.route("/")
@login_required
def list_view():
    studios = list_favorites_for_user(session["user_id"])
    return render_template("favorites.html", studios=studios)


@bp.route("/<int:studio_id>/toggle", methods=["POST"])
@login_required
def toggle(studio_id):
    user_id = session["user_id"]
    if is_favorited(user_id, studio_id):
        remove_favorite(user_id, studio_id)
    else:
        add_favorite(user_id, studio_id)
    return redirect(request.referrer or url_for("search.home"))