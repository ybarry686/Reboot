import requests

from config import Config

SERPAPI_URL = "https://serpapi.com/search"


def search_local_businesses(query, location, api_key=None, limit=10):
    key = api_key or Config.SERPAPI_KEY
    if not key:
        raise RuntimeError("SERPAPI_KEY is not set -- add it to .env before fetching studios.")

    params = {
        "engine": "google_maps",
        "q": f"{query} in {location}",
        "type": "search",
        "api_key": key,
    }

    try:
        resp = requests.get(SERPAPI_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError) as exc:
        print(f"[serpapi_client] request failed for '{query}' near '{location}': {exc}")
        return []

    results = data.get("local_results", [])
    normalized = []
    for r in results[:limit]:
        gps = r.get("gps_coordinates", {})
        normalized.append(
            {
                "name": r.get("title"), "address": r.get("address"),
                "lat": gps.get("latitude"), "lng": gps.get("longitude"),
                "phone": r.get("phone"), "rating": r.get("rating"),
                "place_id": r.get("place_id") or r.get("data_id"), "website": r.get("website"),
            }
        )
    return normalized