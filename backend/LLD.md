# Backend — Low-Level Design

## Module: `app.py`

Single-file Flask application.

### Layers

1. **Database** — `init_db()` creates tables and seeds the demo user on startup via `sqlite3`.
2. **Routes**:
   - `POST /api/login` — looks up user, verifies hashed password, creates a UUID session token.
   - `GET /api/me` — validates `Authorization: Bearer <token>`, returns the associated username.
3. **Static serving** — mounts `../frontend/` at `/` so the whole app runs from one server.

### Key decisions

- Passwords hashed with `werkzeug.security` (`pbkdf2`).
- Session tokens are random UUIDs stored in the `sessions` table.
- SQLite DB file is `users.db`, created in the backend directory.
- CORS enabled for dev convenience.
- `get_db()` opens a per-request connection (simple, no pool needed for a demo).
