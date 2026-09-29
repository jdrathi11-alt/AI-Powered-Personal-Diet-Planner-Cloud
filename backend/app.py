import logging
from pathlib import Path
from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.config import ROOT, CORS_ORIGINS, MAX_CONTENT_LENGTH_MB
from backend.db import init_db
from backend.routes.api import api

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = Flask(__name__, static_folder=str(ROOT / "frontend"))
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH_MB * 1024 * 1024

CORS(app, resources={r"/api/*": {"origins": CORS_ORIGINS.split(",")}})

init_db()
app.register_blueprint(api)

@app.get("/")
def index():
    return send_from_directory(ROOT / "frontend", "index.html")

@app.get("/<path:path>")
def frontend_files(path):
    candidate = ROOT / "frontend" / path
    if candidate.exists() and candidate.is_file():
        return send_from_directory(ROOT / "frontend", path)
    return send_from_directory(ROOT / "frontend", "index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
