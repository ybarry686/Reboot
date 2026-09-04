# Database Design

## Entities and relationships

Reboot uses a SQLite database with SQLAlchemy ORM models. The schema supports users, studios, services, bookings, and favorites.

### Tables

#### `users`
- `id`: integer primary key
- `name`: text
- `email`: text, unique
- `password_hash`: text
- `created_at`: timestamp

#### `studios`
- `id`: integer primary key
- `name`: text
- `address`: text
- `lat`, `lng`: float coordinates
- `phone`: text
- `description`: text
- `category_tags`: text
- `rating`: float
- `source`: text (`manual` or `serpapi`)
- `source_place_id`: text
- `created_at`: timestamp

#### `services`
- `id`: integer primary key
- `studio_id`: foreign key → `studios.id`
- `name`: text
- `category_tags`: text
- `duration_min`: integer
- `price_cents`: integer
- `description`: text

#### `bookings`
- `id`: integer primary key
- `user_id`: foreign key → `users.id`
- `service_id`: foreign key → `services.id`
- `start_time`: timestamp
- `status`: text (`requested`, `cancelled`, etc.)
- `created_at`: timestamp

#### `favorites`
- `id`: integer primary key
- `user_id`: foreign key → `users.id`
- `studio_id`: foreign key → `studios.id`
- `created_at`: timestamp
- unique constraint on `(user_id, studio_id)`

## Relationship diagram

- `users` 1-to-many `bookings`
- `users` 1-to-many `favorites`
- `studios` 1-to-many `services`
- `studios` 1-to-many `favorites`
- `services` 1-to-many `bookings`

## Data flow and integrity

- `Services.studio_id` is CASCADE deleted when its parent `Studio` is removed.
- `Bookings.user_id` and `Bookings.service_id` are CASCADE deleted when the referenced `User` or `Service` is removed.
- `Favorites` also cascade on `user_id` and `studio_id`.
- Foreign key enforcement is enabled with SQLite PRAGMA on connect.

## Query patterns

### Search and listing
- Studios filtered by `category_tags`, `name`, `address`, or `description`.
- Services loaded by `studio_id` for detail pages.

### Booking
- Booking records join `Bookings`, `Services`, and `Studios` to show user-facing appointment details.
- Bookings are cancellable by the user who created them.

### Favorites
- Favorite studios are resolved by joining `Favorites` to `Studios`.
- Duplicate favorites are prevented by a unique constraint.

## Extension points

This schema can be extended for production use with:
- normalized category tables instead of comma-separated tag fields
- separate pricing and availability tables for dynamic appointment slots
- support for provider accounts and studio owners
- improved audit fields and soft deletes
