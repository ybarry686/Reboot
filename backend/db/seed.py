import json
import os

from db.connection import session_scope
from db.models import Services, Studios, init_db

SEED_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed_data.json")


def load_seed_file(path=SEED_FILE):
    with open(path) as f:
        data = json.load(f)
    return data if isinstance(data, list) else data["studios"]


def seed_studios(studios):
    added, skipped = 0, 0
    with session_scope() as session:
        for studio in studios:
            exists = (
                session.query(Studios)
                .filter(Studios.name == studio["name"], Studios.address == studio["address"])
                .first()
            )
            if exists:
                skipped += 1
                continue

            studio_row = Studios(
                name=studio["name"],
                address=studio["address"],
                lat=studio.get("lat"),
                lng=studio.get("lng"),
                phone=studio.get("phone"),
                description=studio.get("description"),
                category_tags=studio["category_tags"],
                rating=studio.get("rating"),
                source=studio.get("source", "manual"),
                source_place_id=studio.get("source_place_id"),
            )
            session.add(studio_row)
            session.flush()

            for service in studio.get("services", []):
                session.add(
                    Services(
                        studio_id=studio_row.id,
                        name=service["name"],
                        category_tags=service["category"],
                        duration_min=service["duration_min"],
                        price_cents=service["price_cents"],
                        description=service.get("description", ""),
                    )
                )
            added += 1
    return added, skipped


if __name__ == "__main__":
    init_db()
    studios = load_seed_file()
    added, skipped = seed_studios(studios)
    print(f"Seeded {added} studios ({skipped} already present, skipped).")