# Round 1 — Backend Reply

## Status: Done

## What was delivered

1. **`app.py`** — Flask application with:
   - `POST /api/login` — validates credentials against SQLite, returns UUID token
   - `GET /api/me` — validates bearer token, returns username
   - Auto-creates tables and seeds demo user (`demo` / `demo1234`) on startup
   - Serves `frontend/` as static files at `/`
   - CORS enabled

2. **`requirements.txt`** — Flask, flask-cors, werkzeug

3. **`LLD.md`** — Low-level design describing module structure

## Decisions

- Single-file app (simple demo, no need for blueprints)
- Per-request DB connections via Flask `g` object
- `users.db` stored in the backend directory
- Passwords hashed with werkzeug's default `pbkdf2` method
- Fallback to `login.html` for unrecognized frontend routes

## Notes

- Could not run integration tests — pip is unavailable in this environment. Syntax has been verified.
