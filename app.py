import json
import logging
import os
import time
from datetime import datetime, timezone

import psycopg2
from flask import Flask, Response, jsonify

app = Flask(__name__)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
app.logger.handlers.clear()
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
app.logger.propagate = False

START_TIME = time.time()

def database_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "apex"),
        user=os.getenv("DB_USER", "apex_user"),
        password=os.getenv("DB_PASSWORD", ""),
        connect_timeout=2,
    )

@app.get("/")
def index():
    app.logger.info("root endpoint requested")
    return jsonify({
        "service": "Apex Operations API",
        "version": os.getenv("APP_VERSION", "dev"),
        "status": "running",
    })

@app.get("/health")
def health():
    # Liveness: checks that the application process can answer requests.
    return jsonify({"status": "healthy"}), 200

@app.get("/ready")
def ready():
    # Readiness: the app is ready only when its database dependency responds.
    try:
        with database_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return jsonify({"status": "ready", "dependency": "database"}), 200
    except Exception as exc:
        app.logger.error("readiness check failed: %s", type(exc).__name__)
        return jsonify({"status": "not_ready", "dependency": "database"}), 503

@app.get("/metrics")
def metrics():
    uptime = max(0, int(time.time() - START_TIME))
    body = (
        "# HELP apex_api_uptime_seconds Seconds since process start\n"
        "# TYPE apex_api_uptime_seconds gauge\n"
        f"apex_api_uptime_seconds {uptime}\n"
    )
    return Response(body, mimetype="text/plain; version=0.0.4")

if __name__ == "__main__":
    # Flask's development server is acceptable for this local assessment demo;
    # a production deployment should use a production WSGI server.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
