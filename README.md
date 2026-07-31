# RecoveryHub

A polished recovery studio discovery and booking platform designed for busy professionals who want to find saunas, cold plunges, massage therapy, and other recovery services in one place.

## Why RecoveryHub?

Many recovery providers are scattered across local listings, studio pages, and marketplace directories. RecoveryHub centralizes:

- searchable recovery studio discovery
- service listings and pricing details
- booking requests for individual sessions
- saved favorites for quick return visits
- studio import from live local-business search
- optional AI-assisted recommendations for recovery goals

## Key features

- Search studios by category, keyword, or ZIP code
- Studio detail view with service offerings and booking form
- Session-based authentication for registration and login
- User profile management
- Favorites list for tracking preferred studios
- Booking request workflow and cancellation
- Data import from SerpApi with studio and default service creation
- Optional Gemini-powered recommendation text

## Architecture overview

RecoveryHub is built with:

- Python 3
- Flask as the web framework
- SQLAlchemy ORM with SQLite for persistence
- Server-rendered HTML templates for the frontend
- External service integration for data import and recommendations

The codebase is separated into clear layers:

- `backend/app.py`: Flask application factory
- `backend/config.py`: environment-driven configuration
- `backend/db/`: database connection, models, and query logic
- `backend/routes/`: route blueprints grouped by domain
- `backend/services/`: business logic and external API wrappers
- `frontend/templates/`: rendered HTML pages
- `frontend/static/`: CSS styles
- `docs/`: architecture, database design, API reference, and user flows

## Database model

Core domain objects:

- `User`
- `Studio`
- `Service`
- `Booking`
- `Favorite`

The schema supports:

- one-to-many relationships from studios to services
- user bookings tied to service appointments
- user favorites tied to studios

## Installation

1. Clone the repository:

```bash
git clone <repo-url> recoveryhub
cd recoveryhub
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the repository root with values such as:

```env
SECRET_KEY=your-secret-key
DATABASE_PATH=backend/db/recoveryhub.db
SERPAPI_KEY=your-serpapi-key
GEMINI_API_KEY=your-gemini-key
HOME_LAT=40.7410
HOME_LNG=-73.9896
```

## Running locally

```bash
python backend/app.py
```

Open `http://127.0.0.1:5000` in your browser.

## How the app works

- The Flask app is initialized in `backend/app.py`.
- The database schema is created automatically on startup.
- Views are exposed through blueprint routes and rendered with Jinja templates.
- Protected routes use session state to verify logged-in users.
- Studios are imported from SerpApi and optionally annotated with AI recommendations.

## Deployment guidance

For production, run behind a WSGI server such as Gunicorn:

```bash
gunicorn --bind 0.0.0.0:8000 backend.app:app
```

Recommended production improvements:

- Replace SQLite with PostgreSQL or MySQL
- Store session secrets in a secure vault
- Add HTTPS / TLS termination
- Add structured logging and request monitoring
- Add booking availability and provider confirmation workflows
- Add automated tests and CI checks

## Documentation

See the `docs/` folder for:

- `architecture.md`
- `database-design.md`
- `api-overview.md`
- `user-flow.md`

## Contributing

Contributions are welcome. Suggested next improvements:

- Add unit and integration tests
- Add provider/studio owner account management
- Improve booking availability modeling
- Convert tag fields into normalized category tables
- Add a REST or GraphQL API layer for mobile clients
