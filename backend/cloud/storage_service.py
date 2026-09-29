import os
from pathlib import Path
from werkzeug.utils import secure_filename
from backend.config import ROOT, STORAGE_MODE, UPLOAD_FOLDER, SUPABASE_BUCKET, SUPABASE_URL, SUPABASE_SERVICE_KEY

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".json", ".txt", ".pdf"}

def allowed(filename):
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

def save_file(file_storage, user_id):
    if not file_storage or not file_storage.filename:
        raise ValueError("No file selected.")
    if not allowed(file_storage.filename):
        raise ValueError("Unsupported file type.")

    safe = secure_filename(file_storage.filename)
    if not safe:
        raise ValueError("Invalid filename.")

    if STORAGE_MODE == "supabase" and SUPABASE_URL and SUPABASE_SERVICE_KEY:
        from supabase import create_client
        client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        path = f"user-{user_id}/{safe}"
        data = file_storage.read()
        client.storage.from_(SUPABASE_BUCKET).upload(
            path, data, {"content-type": file_storage.mimetype or "application/octet-stream"}
        )
        return path

    user_dir = ROOT / UPLOAD_FOLDER / f"user-{user_id}"
    user_dir.mkdir(parents=True, exist_ok=True)
    target = user_dir / safe
    file_storage.save(target)
    return str(target.relative_to(ROOT))

def delete_file(storage_path):
    if STORAGE_MODE == "supabase" and SUPABASE_URL and SUPABASE_SERVICE_KEY:
        from supabase import create_client
        client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        client.storage.from_(SUPABASE_BUCKET).remove([storage_path])
        return

    path = ROOT / storage_path
    if path.exists():
        path.unlink()
