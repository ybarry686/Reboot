from db.models import *
import db.connection as db_con

import unittest, sys
from db.queries.user_queries import *
from db.queries.booking_queries import *
from db.queries.favorite_queries import *
from config import Config

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.pool import StaticPool
from datetime import datetime


sys.path.append('../recoveryhub') # imports python file from parent directory
test_db = "test_db"

# Note: database prepopulated by seed.py script

class DBTests(unittest.TestCase):

    # create priv db engine
    def setUp(self):
        # init db (don't think this is necessary bc methods already do that)
        #self.test_engine = create_engine(f"sqlite:///:memory:", poolclass=StaticPool) #persistent engine use throughout test casese
        self.test_engine = create_engine(f"sqlite:///:memory:", connect_args={"check_same_thread":False}, poolclass=StaticPool) #persistent engine use throughout test casese

        Base.metadata.create_all(self.test_engine)

        # get this test database instead of the real oen
        self.original_session = db_con.SessionLocal
        db_con.SessionLocal = sessionmaker(bind=self.test_engine)

        self.seed_data()
        #SessionLocal = sessionmaker(bind=engine)
        #self.session = SessionLocal()
        #self.app = app.test_client() # create Flask’s test client

    def tearDown(self): # runs after each test case to erase the temp data
        db_con.SessionLocal = self.original_session
        self.test_engine.dispose()
        #self.session.close()
    

    def seed_data(self):
        session = db_con.SessionLocal()

        studio1 = Studios(
            name="Zen Float Studio",
            address="123 Main St, Austin, TX",
            lat=30.2672,
            lng=-97.7431,
            phone="512-555-0100",
            description="Float tank and infrared sauna recovery studio",
            category_tags="float,sauna"
        )

        studio2 = Studios(
            name="Recharge Sports Recovery",
            address="456 Congress Ave, Austin, TX",
            lat=30.2650,
            lng=-97.7440,
            phone="512-555-0101",
            description="Massage and cryotherapy for athletes",
            category_tags="massage,cryo"
        )

        session.add_all([studio1, studio2])
        session.commit()  # commit here so studio1.id and studio2.id get assigned

        service1 = Services(
            studio_id=studio1.id,
            name="60-Min Float Session",
            category_tags="float",
            duration_min=60,
            price_cents=8000,
            description="Sensory deprivation float tank"
        )

        service2 = Services(
            studio_id=studio2.id,
            name="Deep Tissue Massage",
            category_tags="massage",
            duration_min=45,
            price_cents=9500,
            description="Targeted deep tissue massage for muscle recovery"
        )

        
        session.add_all([service1, service2])
        
        session.commit()
        session.close()


    # user query test
    def test_user(self):
        id = create_user("hello", "hello@gmail.com", "world")
        user = get_user_by_id(id)
        #user = get_user_by_email("hello@gmail.com")
        self.assertIsNotNone(user)
        self.assertEqual(user.get("name"), "hello")

    def test_booking(self):
        booking = create_booking(user_id=1, service_id=1, start_time=datetime(2027, 10, 4, 12, 00))
        b = get_booking_by_id(1)
        self.assertEqual(booking, b.get("id"))

    def test_favorites(self):
        add_favorite(1, 1)
        is_fav = is_favorited(1, 1)
        self.assertTrue(is_fav)


if __name__ == "__main__":
    unittest.main()






