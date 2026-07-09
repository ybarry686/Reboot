from flask import Blueprint, render_template, request

from services.search_client import find_studios
from services.gemini_client import get_recommendation
from db.queries.search_queries import get_services_for_studio

bp = Blueprint("search", __name__)


@bp.route("/")
def home():
    category = request.args.get("category") or None
    keyword = request.args.get("q") or None
    goal = request.args.get("goal") or None
    zip_code = request.args.get("zip") or None

    studios = find_studios(category=category, keyword=keyword, zip_code=zip_code)
    for studio in studios:
        studio["services"] = [dict(s) for s in get_services_for_studio(studio["id"])]

    recommendation = None
    if goal:
        recommendation = get_recommendation(goal, studios[:5])

    return render_template(
        "home.html",
        studios=studios, category=category, keyword=keyword or "",
        goal=goal or "", zip_code=zip_code or "", recommendation=recommendation,
    )