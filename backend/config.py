import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
DATABASE_MODE = os.getenv("DATABASE_MODE", "sqlite").lower()
SQLITE_PATH = os.getenv("SQLITE_PATH", "instance/diet_planner.db")
STORAGE_MODE = os.getenv("STORAGE_MODE", "local").lower()
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "storage")
MAX_CONTENT_LENGTH_MB = int(os.getenv("MAX_CONTENT_LENGTH_MB", "5"))

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "diet-plans")

AI_API_URL = os.getenv("AI_API_URL", "")
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "")

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

ROOT.joinpath("instance").mkdir(exist_ok=True)
ROOT.joinpath(UPLOAD_FOLDER).mkdir(exist_ok=True)
