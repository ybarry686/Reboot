# Reboot 🧘

An adaptive recovery marketplace that leverages user lifestyle metrics to deliver context-aware, personalized recovery service recommendations and appointment bookings.

![Terminal Prompt Preview](assets/reboot_home.png)

## 💡Why Reboot?

Many recovery providers are scattered across local listings, studio pages, and marketplace directories. Reboot centralizes:

- searchable recovery studio discovery
- service listings and pricing details
- booking requests for individual sessions
- saved favorites for quick return visits
- studio import from live local-business search
- optional AI-assisted recommendations for recovery goals

## ✨ Key features

- Search studios by category, keyword, or ZIP code
- Studio detail view with service offerings and booking form
- Favorites list for tracking preferred studios
- Booking request workflow and cancellation
- Data import from SerpApi with studio and default service creation
- Optional Gemini-powered recommendation text

## 🏗️ Architecture overview

Reboot is built with:

- Python 3
- Flask as the web framework
- SQLAlchemy ORM with SQLite for persistence
- Server-rendered HTML templates and CSS for the frontend
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


## 🚀 Quick Start

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
DATABASE_PATH=backend/db/reboot.db
SERPAPI_KEY=your-serpapi-key
GEMINI_API_KEY=your-gemini-key
HOME_LAT=40.7410
HOME_LNG=-73.9896
```

## 💻 Running locally

```bash
python backend/app.py
```

Open `http://127.0.0.1:5000` in your browser.


## 🌐 Deployment guidance

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

## 📚 Documentation

See the `docs/` folder for:

- `architecture.md`
- `database-design.md`
- `api-overview.md`
- `user-flow.md`
