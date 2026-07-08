import sqlalchemy as db
from sqlalchemy import create_engine, Column, Integer, String, Float, TIMESTAMP, func, ForeignKey, MetaData
import sqlite3
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# database connection
engine = db.create_engine("sqlite:///fitness_app.db")
Base = declarative_base()


# i guess the below stuff will go in models


'''
conn = sqlite3.connect('fitness_app')
c = conn.cursor()

def create_tables():
    # allow for foreign key support
    c.execute("PRAGMA foreign_keys = ON;")

    # create tables for info database

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """) # user credentials

    c.execute("""
    CREATE TABLE IF NOT EXISTS studios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT,
        lat REAL,
        lng REAL,
        phone TEXT,
        description TEXT,
        source_place_id TEXT,
        category_tags TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """) # 

    c.execute("""
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        studio_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        category TEXT,
        duration_min INTEGER,
        price_cents INTEGER,
        description TEXT,
        FOREIGN KEY (studio_id) REFERENCES studios(id)
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        service_id INTEGER NOT NULL,
        start_time TIMESTAMP NOT NULL,
        status TEXT DEFAULT 'confirmed',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (service_id) REFERENCES services(id)
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        studio_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (studio_id) REFERENCES studios(id)
    );
    """)


    conn.commit()
    conn.close()
'''