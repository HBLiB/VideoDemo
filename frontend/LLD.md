# Low-Level Design — Frontend

## File Structure

```
frontend/
├── LLD.md         # This file
├── login.html     # Login page with credentials form
└── home.html      # Protected greeting page
```

## Approach

- **Vanilla HTML/CSS/JS** — no frameworks or build tools. Each page is a self-contained HTML file with embedded `<style>` and `<script>` tags.
- **Auth flow** — `login.html` POSTs JSON to `/api/login`, stores the returned token in `sessionStorage`, and redirects to `home.html`. `home.html` reads the token from `sessionStorage`, calls `GET /api/me`, and displays a greeting. If no token or 401, redirects back to `login.html`.
- **Logout** — clears `sessionStorage` and redirects to `login.html`.
- **Error handling** — login failures display an inline error message below the form. Network errors show a generic message.
- **Styling** — minimal, centered card layout for both pages.
