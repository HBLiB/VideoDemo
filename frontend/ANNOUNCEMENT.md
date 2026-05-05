# Round 2 — Visual Polish & Micro-interactions

## Goal

Make the frontend feel **fancy and modern**. The current pages are functional but plain — white cards on a grey background with minimal styling. This round is purely cosmetic/UX; no new features, no API changes.

## Scope

You own **`frontend/`** only. Do not touch `backend/`. The two pages (`login.html`, `home.html`) and any new CSS/JS files you add must stay inside `frontend/`.

## Concrete Deliverables

### 1. Modern Visual Design
- Replace the flat grey background with a subtle **gradient or animated background** (e.g. soft gradient shift, mesh gradient, or subtle particle/grain effect).
- Upgrade the card component: add a **glassmorphism or soft-shadow elevation** effect, smooth rounded corners, and subtle border.
- Use a more refined **color palette** — keep the indigo primary but add complementary accent colors and improve contrast.
- Improve **typography**: use `Inter` or another clean Google Font; add proper heading hierarchy and letter-spacing.

### 2. Micro-interactions & Animations
- **Page load**: fade-in / slide-up entrance animation for the card.
- **Input focus**: smooth border-color transition and subtle glow on focus.
- **Button hover/active**: scale + shadow transition on hover; press-down effect on active.
- **Form submit**: brief loading spinner or pulse animation on the button while the request is in flight.
- **Error messages**: slide-down / fade-in animation when errors appear.
- **Login success**: brief success flash or check animation before redirect.
- **Home page greeting**: typewriter or fade-in effect for the welcome message.

### 3. UX Polish
- Add a **VideoDemo logo or icon** at the top of the login card (can be a styled SVG or CSS-only logo).
- Add a subtle **footer** with "VideoDemo © 2026" or similar.
- Ensure the design is **responsive** and looks good on mobile.
- Add **:focus-visible** outlines for keyboard accessibility.
- Smooth **transitions** on all interactive elements (200-300ms ease).

## Constraints
- Keep it **vanilla HTML + CSS + JS** — no frameworks, no build tools.
- You may add a `<link>` to Google Fonts CDN.
- All CSS can live inline in `<style>` or in a new `frontend/styles.css` file (your call).
- All JS can live inline or in a new `frontend/app.js` file (your call).
- Do **not** change the API contract (endpoints, request/response shapes, token storage logic).
- The functional behavior (login flow, redirect, greeting, logout) must remain identical.

## Definition of Done
- Both pages look noticeably more polished and modern.
- Animations are smooth (no jank) and tasteful (not distracting).
- The pages still work correctly: login, redirect, greeting, logout.
- Reply with `REPLY.md` summarizing what you changed.
