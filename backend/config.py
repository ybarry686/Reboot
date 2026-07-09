import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(os.path.dirname(BASE_DIR), ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH", os.path.join(BASE_DIR, "db", "recoveryhub.db")
    )
    SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    HOME_LAT = float(os.environ.get("HOME_LAT", "40.7410"))
    HOME_LNG = float(os.environ.get("HOME_LNG", "-73.9896"))