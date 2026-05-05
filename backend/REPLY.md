# Security Audit — VideoDemo

## Summary

The codebase is a small demo app with reasonable basics (parameterized SQL, hashed passwords, UUID tokens) but has several issues that would be **critical in any production context**: debug mode enabled, no session expiry, a hardcoded default credential, no rate limiting, overly permissive CORS, and potential XSS via unsanitized username rendering.

## Findings

### [CRITICAL] — Debug Mode Enabled in Production Entrypoint

- **Location:** `backend/app.py:97` — `app.run(debug=True, port=5000)`
- **Issue:** Flask debug mode is hardcoded to `True`. Debug mode enables the Werkzeug interactive debugger, which allows **arbitrary code execution** on the server if an attacker can trigger an exception.
- **Risk:** Full remote code execution (RCE) on the server. The debugger exposes a Python REPL in the browser.
- **Recommendation:** Set `debug=False` for any non-local use, or read from an environment variable: `app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")`.

### [CRITICAL] — No Session Expiry or Invalidation

- **Location:** `backend/app.py:56–62` (token creation), `backend/app.py:67–80` (`/api/me` token lookup)
- **Issue:** Session tokens are created with a `created` timestamp but are **never expired or cleaned up**. There is no logout endpoint. Tokens live forever in the `sessions` table.
- **Risk:** A stolen token grants permanent access. Session accumulation also constitutes a slow resource leak in the DB.
- **Recommendation:** Add a TTL check (e.g., reject tokens older than 24h), add a `DELETE /api/logout` endpoint, and run periodic cleanup of expired sessions.

### [HIGH] — Hardcoded Default Credentials (Seed User)

- **Location:** `backend/app.py:47–50` — `("demo", generate_password_hash("demo1234"))`
- **Issue:** The demo user `demo` / `demo1234` is seeded on every startup. The credentials are in plaintext in the source code and trivially guessable.
- **Risk:** Anyone who reads the source or guesses the credential has instant access. If this code reaches production, the account is an open door.
- **Recommendation:** Remove the seed user from production builds, or at minimum gate it behind an environment variable (e.g., `SEED_DEMO_USER=true`).

### [HIGH] — No Rate Limiting on Login

- **Location:** `backend/app.py:54–62` — `POST /api/login`
- **Issue:** There is no rate limiting, account lockout, or throttling on the login endpoint.
- **Risk:** An attacker can brute-force passwords at full speed. With the weak demo password (`demo1234`), this is trivial.
- **Recommendation:** Add rate limiting (e.g., `flask-limiter`) — something like 5 attempts per minute per IP on `/api/login`.

### [HIGH] — Overly Permissive CORS

- **Location:** `backend/app.py:10` — `CORS(app)`
- **Issue:** `CORS(app)` with no arguments defaults to allowing **all origins** (`Access-Control-Allow-Origin: *`). This means any website can make authenticated API requests to this backend.
- **Risk:** A malicious site can call `/api/login` or `/api/me` from a user's browser. Combined with token theft, this enables cross-origin attacks.
- **Recommendation:** Restrict to specific origins: `CORS(app, origins=["http://localhost:5000"])`, or remove CORS entirely since the frontend is served from the same origin.

### [MEDIUM] — Potential XSS via Username in Greeting

- **Location:** `frontend/home.html:42` — `typewrite(greetingEl, 'Welcome, ' + data.username + '!', 50);`
- **Issue:** The username from the API is concatenated into text rendered via `el.textContent`. While `textContent` is safe against HTML injection, this relies on the current implementation detail. If the rendering ever changes to `innerHTML` (e.g., to add formatting), it becomes exploitable. Additionally, there is no server-side validation of username characters during registration (no registration endpoint exists yet, but the schema allows any string).
- **Risk:** Currently low due to `textContent` usage, but a fragile defense. If a username containing `<script>` tags were inserted into the DB and rendering changed, it would be exploitable.
- **Recommendation:** Validate and sanitize usernames on the backend (alphanumeric only, length limit). This is defense-in-depth.

### [MEDIUM] — No HTTPS Enforcement

- **Location:** `backend/app.py:97` — `app.run(debug=True, port=5000)` (plain HTTP)
- **Issue:** The server runs on plain HTTP. Tokens are transmitted in `Authorization` headers and login credentials in POST bodies without transport encryption.
- **Risk:** Network eavesdropping (MITM) can capture tokens and credentials in transit.
- **Recommendation:** In production, terminate TLS via a reverse proxy (nginx, Caddy) or configure Flask with SSL certificates. Add `Strict-Transport-Security` header.

### [MEDIUM] — Missing Security Headers

- **Location:** All responses from `backend/app.py`
- **Issue:** No security-related HTTP headers are set: no `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`, `Strict-Transport-Security`, or `Referrer-Policy`.
- **Risk:** The app is more susceptible to clickjacking, MIME sniffing, and other browser-based attacks.
- **Recommendation:** Add a middleware or use `flask-talisman` to set: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Content-Security-Policy: default-src 'self'`, `Referrer-Policy: strict-origin-when-cross-origin`.

### [MEDIUM] — No `SECRET_KEY` Configured for Flask

- **Location:** `backend/app.py` — no `app.secret_key` or `app.config['SECRET_KEY']` set
- **Issue:** Flask's `SECRET_KEY` is not set. While this app doesn't use Flask sessions or CSRF tokens, the absence means any future use of `flask.session` or CSRF protection will silently use an insecure default.
- **Risk:** Low today, but a latent vulnerability if Flask sessions are added later.
- **Recommendation:** Set `app.secret_key = os.urandom(32)` or read from an environment variable.

### [LOW] — Session Tokens Stored in `sessionStorage` (Frontend)

- **Location:** `frontend/login.html:56` — `sessionStorage.setItem('token', data.token);`
- **Issue:** `sessionStorage` is accessible to any JavaScript running on the same origin. If an XSS vulnerability is introduced, tokens can be stolen.
- **Risk:** Token theft via XSS. Using `sessionStorage` is acceptable for a demo, but `HttpOnly` cookies would be more secure.
- **Recommendation:** For production, consider switching to `HttpOnly` + `Secure` + `SameSite=Strict` cookies for token storage, which are inaccessible to JavaScript.

### [LOW] — Dependency Versions Not Pinned Exactly

- **Location:** `backend/requirements.txt`
- **Issue:** Dependencies use `>=` minimum versions (`Flask>=3.0`, `flask-cors>=4.0`, `werkzeug>=3.0`) rather than exact pins.
- **Risk:** A future `pip install` could pull in a version with a vulnerability or breaking change. Supply-chain risk.
- **Recommendation:** Pin exact versions (e.g., `Flask==3.1.0`) and use `pip-audit` or Dependabot to track CVEs.

### [LOW] — No Input Length Validation

- **Location:** `backend/app.py:55–56` — `username = data.get("username", "")`, `password = data.get("password", "")`
- **Issue:** No maximum length is enforced on username or password inputs. An attacker could send a multi-megabyte password to consume hashing CPU time.
- **Risk:** Denial-of-service via expensive `pbkdf2` hashing on very long passwords.
- **Recommendation:** Cap password length at a reasonable limit (e.g., 128 characters) before hashing.

### [LOW] — Google Fonts Loaded from External CDN Without Integrity

- **Location:** `frontend/styles.css:2` — `@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');`
- **Issue:** An external resource is loaded without a Subresource Integrity (SRI) hash. CSS `@import` does not support SRI, so the font would need to be loaded via a `<link>` tag to use `integrity`.
- **Risk:** If Google Fonts CDN is compromised, malicious CSS could be injected. Low probability but non-zero.
- **Recommendation:** Self-host the font, or load it via `<link>` with an SRI `integrity` attribute.

## Positive Observations

- **Parameterized SQL queries throughout** — all `db.execute()` calls use `?` placeholders, preventing SQL injection. Well done.
- **Password hashing with `werkzeug.security`** — uses `pbkdf2` with salt, which is a solid choice for a demo.
- **UUID4 session tokens** — cryptographically random, not guessable.
- **`textContent` used for DOM rendering** — the frontend avoids `innerHTML`, preventing the most common XSS vector.
- **Consistent error responses** — login failures return a generic "Invalid credentials" message, not leaking whether the username exists (though timing differences could still be observed).
- **Clean separation of concerns** — frontend and backend are cleanly separated with a JSON API contract.
