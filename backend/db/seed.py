import json
import os
from models import Studios, init_session, exists

folder = os.path.dirname(__file__)
json_path = os.path.join(folder, "seed_data.json")

with open(json_path) as f:
    studios = json.load(f)

session = init_session()

for s in studios:
    if exists(session, Studios, source_place_id=s["source_place_id"]):
        continue
    studio = Studios(
        name=s["name"],
        address=s["address"],
        lat=s["lat"],
        lng=s["lng"],
        phone=s["phone"],
        description=s["description"],
        source_place_id=s["source_place_id"],
        category_tags=s["category_tags"],
    )
    session.add(studio)

session.commit()
print("Seeded studios. Total in db:", len(list(session.query(Studios))))