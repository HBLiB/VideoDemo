# Round 1 — Frontend

## Task

Build the frontend for the VideoDemo login app. Read `HLD.md` for full context.

## Deliverables

1. **`frontend/login.html`** — Login page with a form (username + password fields, submit button). On submit, POST JSON to `/api/login`. On success, store the returned `token` in `sessionStorage` and redirect to `home.html`. On failure, show an error message.

2. **`frontend/home.html`** — Protected page. On load, call `GET /api/me` with `Authorization: Bearer <token>` header. If valid, display a greeting ("Welcome, <username>!") and a logout button. If unauthorized or no token, redirect to `login.html`. Logout clears `sessionStorage` and redirects to `login.html`.

3. **`frontend/LLD.md`** — Brief low-level design describing your file structure and approach.

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

- Vanilla HTML + CSS + JavaScript only (no frameworks, no build tools)
- All files must live inside `frontend/`
- Assume the API is at the same origin
- Keep it clean and simple — this is a demo
