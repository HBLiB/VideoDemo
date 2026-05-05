# Round 2 Reply — Visual Polish & Micro-interactions

## What Changed

### New file: `styles.css`
- Shared stylesheet for both pages
- **Animated gradient background** (dark indigo/purple, shifts over 15s)
- **Glassmorphism card**: translucent background, backdrop blur, subtle border, deep shadow
- **Inter** Google Font with proper heading hierarchy, letter-spacing, uppercase labels
- **Input focus**: smooth border-color transition + indigo glow ring
- **Button hover/active**: translateY lift + shadow on hover, scale-down press on active
- **Loading spinner**: CSS-only spinner via `button.loading` class
- **Success flash**: green checkmark via `button.success` class
- **Error animation**: slide-down/fade-in via `.error.visible` class
- **Card entrance**: fade-in + slide-up on page load (cubic-bezier eased)
- **Footer**: fades in after 0.5s delay
- **Typewriter cursor**: blinking accent-colored cursor for greeting text
- **Responsive**: card gets margin + smaller padding on narrow viewports
- **Accessibility**: `:focus-visible` outlines on inputs and buttons
- All transitions 250ms ease

### Updated: `login.html`
- Links shared `styles.css`, removed inline styles
- Added SVG play-button logo + "VideoDemo" gradient text
- Added placeholder text on inputs
- Submit button shows spinner while request is in-flight
- On success: shows green checkmark for 600ms before redirect
- Error messages animate in/out smoothly
- Added footer "VideoDemo © 2026"

### Updated: `home.html`
- Links shared `styles.css`, removed inline styles
- Added same logo component
- Greeting uses **typewriter effect** (50ms per character, cursor blinks then hides)
- Added footer
- Card centered with text-align

## Decisions
- Kept everything vanilla HTML/CSS/JS, no build tools
- Used a single shared CSS file to avoid duplication
- Dark theme chosen for the gradient background — it makes the glassmorphism card pop more than a light background would
- SVG logo is inline (CSS-only, no external assets)
- API contract and auth flow are completely unchanged

## Status
Done — all deliverables complete.
