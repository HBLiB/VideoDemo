# Round 1 — Frontend Reply

## Status: Done

## What I built

1. **`frontend/login.html`** — Login page with username/password form. POSTs JSON to `/api/login`, stores token in `sessionStorage`, redirects to `home.html`. Shows inline error on failure.

2. **`frontend/home.html`** — Protected page. Reads token from `sessionStorage`, calls `GET /api/me` with Bearer header. Displays "Welcome, \<username\>!" greeting and a logout button. Redirects to `login.html` if no token or 401.

3. **`frontend/LLD.md`** — Low-level design describing file structure and approach.

## Decisions

- Self-contained HTML files with embedded `<style>` and `<script>` — no separate CSS/JS files, keeping it minimal for a demo.
- Minimal card-style centered layout for both pages.
- Network errors handled with a generic user-facing message.
