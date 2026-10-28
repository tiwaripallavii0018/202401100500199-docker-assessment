
import os
import psycopg2
from flask import Flask, jsonify, request
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

REGNO = os.getenv("REGNO", "202401100500199")
APP_VERSION = os.getenv("APP_VERSION", "dev")


def connect():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        dbname=os.getenv("DB_NAME", "festpass"),
        user=os.getenv("DB_USER", "festpass"),
        password=os.getenv("DB_PASSWORD", ""),
        connect_timeout=3,
    )


def create_table():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS registrations (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    event TEXT NOT NULL,
                    created TIMESTAMPTZ NOT NULL DEFAULT now()
                )
            """)


@app.route("/api/health", methods=["GET"])
def health():
    database = False
    try:
        create_table()
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        database = True
    except Exception:
        pass

    return jsonify({
        "service": "festpass-backend",
        "regno": REGNO,
        "version": APP_VERSION,
        "database": database
    })


@app.route("/api/registrations", methods=["GET"])
def get_registrations():
    try:
        create_table()
        with connect() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT id, name, event, created "
                    "FROM registrations ORDER BY id"
                )
                rows = cur.fetchall()

        for row in rows:
            row["created"] = row["created"].isoformat(
                timespec="seconds"
            )

        return jsonify(rows)
    except Exception:
        return jsonify({"error": "database unavailable"}), 503


@app.route("/api/registrations", methods=["POST"])
def add_registration():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    event = str(data.get("event", "")).strip()

    if not name or not event:
        return jsonify({
            "error": "name and event are required"
        }), 400

    try:
        create_table()
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO registrations (name, event) "
                    "VALUES (%s, %s) RETURNING id",
                    (name, event)
                )
                registration_id = cur.fetchone()[0]

        return jsonify({
            "id": registration_id,
            "name": name,
            "event": event
        }), 201
    except Exception:
        return jsonify({"error": "database unavailable"}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
