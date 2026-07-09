from config import Config
from db.queries.search_queries import search_studios
from utils.geo import haversine_miles, zip_to_latlng

VALID_CATEGORIES = {"sauna", "cold_plunge", "massage", "cryotherapy", "acupuncture"}


def find_studios(category=None, keyword=None, zip_code=None):
    if category and category not in VALID_CATEGORIES:
        category = None

    rows = search_studios(category=category, keyword=keyword)

    origin_lat, origin_lng = Config.HOME_LAT, Config.HOME_LNG
    if zip_code:
        zip_lat, zip_lng = zip_to_latlng(zip_code)
        if zip_lat is not None:
            origin_lat, origin_lng = zip_lat, zip_lng

    studios = []
    for row in rows:
        studio = dict(row)
        studio["distance_mi"] = haversine_miles(origin_lat, origin_lng, studio.get("lat"), studio.get("lng"))
        studios.append(studio)

    studios.sort(key=lambda s: (s["distance_mi"] is None, s["distance_mi"] or 0))
    return studios