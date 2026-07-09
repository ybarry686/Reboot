import argparse
import json
import os

from services.serpapi_client import search_local_businesses

CATEGORIES = {
    "sauna": "sauna",
    "cold_plunge": "cold plunge ice bath",
    "massage": "massage therapy",
    "stretch": "assisted stretch studio",
}

OUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed_data.json")


def build_studio_records(location, per_category=5):
    studios_by_key = {}
    for category, query in CATEGORIES.items():
        results = search_local_businesses(query, location)
        for r in results[:per_category]:
            key = (r["name"], r["address"])
            if key in studios_by_key:
                existing_tags = set(studios_by_key[key]["category_tags"].split(","))
                existing_tags.add(category)
                studios_by_key[key]["category_tags"] = ",".join(sorted(existing_tags))
                continue
            studios_by_key[key] = {
                "name": r["name"],
                "address": r["address"],
                "lat": r.get("lat"),
                "lng": r.get("lng"),
                "phone": r.get("phone"),
                "description": f"{r['name']} -- recovery studio near {location}.",
                "category_tags": category,
                "rating": r.get("rating"),
                "source": "serpapi",
                "source_place_id": r.get("place_id"),
                "_website_for_manual_lookup": r.get("website"),
                "services": [
                    {
                        "name": f"Standard {category.replace('_', ' ').title()} Session",
                        "category": category,
                        "duration_min": 60,
                        "price_cents": 7000,
                        "description": "Edit this placeholder service with the studio's real pricing/menu.",
                    }
                ],
            }
    return list(studios_by_key.values())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--location", required=True, help='e.g. "Los Angeles, CA"')
    parser.add_argument("--per-category", type=int, default=5)
    args = parser.parse_args()

    studios = build_studio_records(args.location, args.per_category)
    with open(OUT_FILE, "w") as f:
        json.dump({"_comment": f"Fetched via SerpApi for {args.location}", "studios": studios}, f, indent=2)

    print(f"Wrote {len(studios)} studios to {OUT_FILE}")
    print("Now edit each studio's `services` list with real names/prices, then run: python -m db.seed")