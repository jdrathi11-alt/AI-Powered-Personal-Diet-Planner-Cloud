"""
Cloud database adapter.

Local mode uses SQLite through backend.models.
Cloud mode demonstrates the Supabase Python client. The backend service key,
when used, must remain server-side and must never be shipped to the browser.
"""

from backend.config import DATABASE_MODE, SUPABASE_URL, SUPABASE_SERVICE_KEY

_supabase = None

def get_supabase():
    global _supabase
    if _supabase is not None:
        return _supabase
    if not (SUPABASE_URL and SUPABASE_SERVICE_KEY):
        return None
    from supabase import create_client
    _supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    return _supabase

def cloud_enabled():
    return DATABASE_MODE == "supabase" and get_supabase() is not None
