# High-Level Design — VideoDemo

## Overview

A small demo website with user authentication and a persistent database. Two pages: a login screen and a protected home page that greets the logged-in user.

## Architecture

```
┌──────────────┐        HTTP        ┌──────────────┐       SQL       ┌──────────────┐
│   Frontend   │  ←───────────────→ │   Backend    │ ←─────────────→ │   SQLite DB  │
│  (static JS) │   JSON API calls   │  (Python)    │                 │  (users.db)  │
└──────────────┘                    └──────────────┘                 └──────────────┘
```

## Components

### Frontend (`frontend/`)

| Item | Choice |
|------|--------|
| Tech | Vanilla HTML + CSS + JavaScript |
| Pages | `login.html` — login form; `home.html` — protected greeting page |
| Auth flow | POST credentials to backend, receive a session token, store in `sessionStorage`, send as `Authorization: Bearer <token>` header |
| Routing | Redirect to `login.html` if no valid token; redirect to `home.html` on successful login |

### Backend (`backend/`)

| Item | Choice |
|------|--------|
| Tech | Python 3 with Flask |
| API prefix | `/api` |
| Endpoints | `POST /api/login` — authenticate, return token; `GET /api/me` — return current user info (protected) |
| Auth | Simple bearer token (UUID issued on login, stored in DB) |
| DB | SQLite via Python `sqlite3` stdlib module — file: `users.db` |
| Startup | Auto-create tables and seed a demo user on first run |

### Database Schema

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

Seed data: one demo user (`demo` / `demo1234`).

## Contracts

### `POST /api/login`

- **Request:** `{ "username": "...", "password": "..." }`
- **Success 200:** `{ "token": "uuid-string" }`
- **Failure 401:** `{ "error": "Invalid credentials" }`

### `GET /api/me`

- **Header:** `Authorization: Bearer <token>`
- **Success 200:** `{ "username": "..." }`
- **Failure 401:** `{ "error": "Unauthorized" }`

## Directory Layout

```
/
├── HLD.md
├── frontend/          # frontend team owns this
│   ├── LLD.md
│   ├── login.html
│   ├── home.html
│   └── ...
├── backend/           # backend team owns this
│   ├── LLD.md
│   ├── app.py
│   ├── requirements.txt
│   └── ...
└── README.md
```

## Running Locally

```bash
# Backend
cd backend && pip install -r requirements.txt && python app.py
# Serves API on http://localhost:5000

# Frontend
# Open frontend/login.html in a browser, or serve with:
cd frontend && python -m http.server 8080
```

The frontend assumes the API is at the same origin (Flask will also serve static files in dev, or use CORS).
