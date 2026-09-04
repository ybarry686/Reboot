# Reboot Architecture

## High-level architecture

Reboot is a Flask-based web application with a monolithic backend and a small static frontend. It is designed to connect users with local recovery studios, enabling search, favorite management, booking requests, and data import from external business search APIs.

### Layers

- **Frontend**
  - Templates: `frontend/templates/*.html`
  - Static assets: `frontend/static/css/styles.css`
  - User-facing views for home search, studio details, login/signup, profile, favorites, bookings, and studio import.

- **Backend**
  - Application entrypoint: `backend/app.py`
  - Configuration: `backend/config.py`
  - Database initialization and ORM models: `backend/db/models.py`
  - DB connection and session management: `backend/db/connection.py`
  - API routes: `backend/routes/*.py`
  - Business logic services: `backend/services/*.py`
  - DB queries and persistence logic: `backend/db/queries/*.py`

- **Data sources**
  - Local SQLite database for users, studios, services, bookings, and favorites.
  - External business search via SerpApi for importing local recovery studios.
  - Optional recommendation generation via Gemini API.

## Application flow

1. `backend/app.py` creates the Flask app and registers route blueprints.
2. `backend/db/models.py` initializes the SQLite schema with SQLAlchemy.
3. User actions in the browser invoke route handlers in `backend/routes/`.
4. Routes use service layer clients in `backend/services/` for authentication, search, booking, and recommendations.
5. Routes persist and query data through query modules in `backend/db/queries/`.

## Key components

- `auth_routes.py`: login, signup, logout.
- `user_routes.py`: profile edit.
- `search_routes.py`: home search, recommendation injection.
- `booking_routes.py`: studio detail, book service, view/cancel bookings.
- `favorites_routes.py`: favorite studio toggle and list.
- `import_routes.py`: studio import from SerpApi.

## Deployment considerations

- Configuration values are sourced from environment variables via `.env`.
- SQLite is used for development and simple deployments.
- The app exports a WSGI-compatible Flask application instance named `app`.
- In production, the app should run behind a WSGI server such as Gunicorn or uWSGI.
