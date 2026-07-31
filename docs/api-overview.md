# API Overview

## Route architecture

The backend exposes a server-rendered Flask web application. Each route blueprint is grouped by feature area:

- `backend/routes/auth_routes.py`
- `backend/routes/user_routes.py`
- `backend/routes/search_routes.py`
- `backend/routes/favorites_routes.py`
- `backend/routes/booking_routes.py`
- `backend/routes/import_routes.py`

## Public endpoints

### `/`
- Method: GET
- Purpose: Search studios and optionally request a recommendation.
- Query params:
  - `category` — recovery service category
  - `q` — search keywords
  - `goal` — recommendation prompt
  - `zip` — ZIP code for distance sorting
- Behavior: returns the home page with matching studios and optional Gemini recommendation.

### `/auth/signup`
- Methods: GET, POST
- Purpose: Register new users.
- POST form fields: `name`, `email`, `password`
- Behavior: creates an account, logs the user in, redirects to `/`.

### `/auth/login`
- Methods: GET, POST
- Purpose: Authenticate existing users.
- POST form fields: `email`, `password`
- Behavior: verifies credentials, stores `user_id` in session, redirects to `/`.

### `/auth/logout`
- Method: GET
- Purpose: End the session and redirect to login.

## Authenticated endpoints

### `/profile/`
- Methods: GET, POST
- Purpose: display and update the current user's profile.
- POST fields: `name`, `email`

### `/favorites/`
- Method: GET
- Purpose: show followed/favorited studios for the logged-in user.

### `/favorites/<int:studio_id>/toggle`
- Method: POST
- Purpose: add or remove a studio from the user's favorites.

### `/studios/<int:studio_id>`
- Method: GET
- Purpose: show studio detail page with services, booking form, and favorite state.

### `/bookings`
- Method: POST
- Purpose: create a booking request for a specific service.
- POST fields: `studio_id`, `service_id`, `start_time`

### `/bookings/mine`
- Method: GET
- Purpose: list the logged-in user's bookings.

### `/bookings/<int:booking_id>/cancel`
- Method: POST
- Purpose: cancel a booking belonging to the current user.

### `/import/`
- Methods: GET, POST
- Purpose: import local studio data from SerpApi.
- POST fields: `location`, `category`
- Behavior: creates a new `Studio` and default `Service` for imported results.

## Service layer responsibilities

- `backend/services/auth_client.py` handles password hashing, signup validation, and login checks.
- `backend/services/user_client.py` fetches and updates user profile data.
- `backend/services/search_client.py` performs studio search and distance sorting.
- `backend/services/booking_client.py` validates start time and places bookings.
- `backend/services/gemini_client.py` calls the Gemini API for recommendation text.
- `backend/services/serpapi_client.py` (external search client) imports local studios from live business search results.

## Data access patterns

- Route handlers delegate persistence to query modules under `backend/db/queries/`.
- Queries open sessions via `db.connection.session_scope()` to ensure commit/rollback semantics.
- SQLAlchemy ORM models are defined in `backend/db/models.py`.

## Authentication and session management

- Flask server-side sessions store `user_id` and `user_name` after login.
- `utils/decorators.py` enforces login on protected routes.
- Secret config values are loaded from `.env` using `python-dotenv`.
