from flask import Blueprint, render_template, request, flash, redirect, url_for

from db.connection import session_scope
from db.models import Services, Studios
from services.serpapi_client import search_local_businesses
from utils.decorators import login_required

bp = Blueprint("import_studios", __name__, url_prefix="/import")

CATEGORY_QUERIES = {
    "sauna": "sauna",
    "cold_plunge": "cold plunge ice bath",
    "massage": "massage therapy",
    "cryotherapy": "cryotherapy",
    "acupuncture": "acupuncture",
}


@bp.route("/", methods=["GET", "POST"])
@login_required
def import_studios():
    if request.method == "POST":
        location = request.form["location"].strip()
        category = request.form["category"]
        query = CATEGORY_QUERIES.get(category, category)

        try:
            results = search_local_businesses(query, location)
        except RuntimeError as exc:
            flash(str(exc), "error")
            return redirect(url_for("import_studios.import_studios"))

        added = 0
        with session_scope() as session:
            for r in results:
                if not r.get("name") or not r.get("address"):
                    continue
                exists = (
                    session.query(Studios)
                    .filter(Studios.name == r["name"], Studios.address == r["address"])
                    .first()
                )
                if exists:
                    continue
                studio = Studios(
                    name=r["name"], address=r["address"], lat=r.get("lat"), lng=r.get("lng"),
                    phone=r.get("phone"), description=f"{r['name']} -- imported live from SerpApi.",
                    category_tags=category, rating=r.get("rating"), source="serpapi",
                    source_place_id=r.get("place_id"),
                )
                session.add(studio)
                session.flush()
                session.add(
                    Services(
                        studio_id=studio.id,
                        name=f"Standard {category.replace('_', ' ').title()} Session",
                        category_tags=category, duration_min=60, price_cents=7000,
                        description="Imported live -- edit with the studio's real pricing.",
                    )
                )
                added += 1

        flash(f"Imported {added} new studio(s) from SerpApi for '{location}'.", "success")
        return redirect(url_for("search.home"))

    return render_template("import_studios.html")