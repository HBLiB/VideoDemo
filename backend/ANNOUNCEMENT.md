# Round 3 — Security Audit (READ-ONLY)

## Goal

Perform a **written security review** of the entire VideoDemo codebase. This is a **read-only** round — **do not change any code, do not create or modify any files other than `backend/REPLY.md`**.

## What to Audit

Read everything in the repo (`backend/`, `frontend/`, `HLD.md`, configs) and assess:

### Backend
1. **Authentication & session management** — token generation, storage, expiry, invalidation
2. **Password handling** — hashing algorithm, salt, strength requirements
3. **Input validation & injection** — SQL injection, command injection, parameter validation
4. **API security** — rate limiting, CORS, error information leakage, HTTP headers
5. **Dependencies** — known vulnerabilities in `requirements.txt` packages, pinned versions
6. **Secrets & config** — hardcoded secrets, debug mode, default credentials
7. **Database** — schema safety, migrations, access control

### Frontend
8. **XSS & content injection** — DOM manipulation, user-controlled content rendering
9. **Token handling** — storage mechanism, exposure risks
10. **External resources** — CDN integrity, mixed content

### General
11. **HTTPS / transport security**
12. **Seed data / default credentials** — demo user risk in production

## Output Format

Write your findings in `backend/REPLY.md` using this structure:

```markdown
# Security Audit — VideoDemo

## Summary
<1-2 sentence overall assessment>

## Findings

### [CRITICAL/HIGH/MEDIUM/LOW] — <Title>
- **Location:** file(s) and line(s)
- **Issue:** what's wrong
- **Risk:** what could happen
- **Recommendation:** how to fix

(repeat for each finding, ordered by severity)

## Positive Observations
<things that are already done well>
```

## Constraints
- **READ-ONLY** — do not modify any file except `backend/REPLY.md`
- Do not create branches, PRs, or code changes
- Be specific: cite file names, line numbers, and code snippets
- Be honest: if something is fine, say so
