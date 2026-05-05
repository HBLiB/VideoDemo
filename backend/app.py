import os
import sqlite3
import uuid

from flask import Flask, g, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.db")
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")


# ── Database helpers ──────────────────────────────────────────────

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "  id       INTEGER PRIMARY KEY AUTOINCREMENT,"
        "  username TEXT    UNIQUE NOT NULL,"
        "  password TEXT    NOT NULL"
        ")"
    )
    db.execute(
        "CREATE TABLE IF NOT EXISTS sessions ("
        "  token    TEXT PRIMARY KEY,"
        "  user_id  INTEGER NOT NULL REFERENCES users(id),"
        "  created  TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        ")"
    )
    # Seed demo user if not present
    existing = db.execute("SELECT id FROM users WHERE username = ?", ("demo",)).fetchone()
    if not existing:
        db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("demo", generate_password_hash("demo1234")),
        )
    db.commit()
    db.close()


# ── API routes ────────────────────────────────────────────────────

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

    if user is None or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = str(uuid.uuid4())
    db.execute("INSERT INTO sessions (token, user_id) VALUES (?, ?)", (token, user["id"]))
    db.commit()
    return jsonify({"token": token})


@app.route("/api/me", methods=["GET"])
def me():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"error": "Unauthorized"}), 401

    token = auth[7:]
    db = get_db()
    row = db.execute(
        "SELECT u.username FROM sessions s JOIN users u ON s.user_id = u.id WHERE s.token = ?",
        (token,),
    ).fetchone()

    if row is None:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({"username": row["username"]})


# ── Static file serving ──────────────────────────────────────────

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path and os.path.isfile(os.path.join(FRONTEND_DIR, path)):
        return send_from_directory(FRONTEND_DIR, path)
    return send_from_directory(FRONTEND_DIR, "login.html")


# ── Entrypoint ────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
