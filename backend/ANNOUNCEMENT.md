# Round 1 — Backend

## Task

Build the backend for the VideoDemo login app. Read `HLD.md` for full context.

## Deliverables

1. **`backend/app.py`** — Flask application implementing:
   - `POST /api/login` — validate credentials, return a UUID token
   - `GET /api/me` — validate bearer token, return username
   - On startup: auto-create tables and seed a demo user (`demo` / `demo1234`) if not present
   - Serve the `frontend/` directory as static files at `/` so everything runs from one server
   - Enable CORS for development convenience

2. **`backend/requirements.txt`** — Python dependencies (Flask, flask-cors, werkzeug)

3. **`backend/LLD.md`** — Brief low-level design describing your module structure and approach.

## Database Schema (from HLD)

```sql
CREATE TABLE users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT    UNIQUE NOT NULL,
    password TEXT    NOT NULL          -- hashed with werkzeug
);

CREATE TABLE sessions (
    token    TEXT PRIMARY KEY,
    user_id  INTEGER NOT NULL REFERENCES users(id),
    created  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Contracts (from HLD)

### `POST /api/login`
- Request: `{ "username": "...", "password": "..." }`
- Success 200: `{ "token": "uuid-string" }`
- Failure 401: `{ "error": "Invalid credentials" }`

### `GET /api/me`
- Header: `Authorization: Bearer <token>`
- Success 200: `{ "username": "..." }`
- Failure 401: `{ "error": "Unauthorized" }`

## Constraints

- Python 3, Flask, SQLite (stdlib `sqlite3`)
- Hash passwords with `werkzeug.security`
- All files must live inside `backend/`
- Keep it clean and simple — this is a demo
