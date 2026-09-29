from datetime import datetime, timezone
from backend.db import one, all_rows, execute
from backend.config import DATABASE_MODE, SUPABASE_URL, SUPABASE_SERVICE_KEY

_supabase = None

def now():
    return datetime.now(timezone.utc).isoformat()

def cloud_client():
    global _supabase
    if _supabase is None:
        if not (SUPABASE_URL and SUPABASE_SERVICE_KEY):
            raise RuntimeError("Supabase mode requires SUPABASE_URL and SUPABASE_SERVICE_KEY")
        from supabase import create_client
        _supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    return _supabase

def cloud():
    return DATABASE_MODE == "supabase"

def create_user(name, email, password_hash):
    if not cloud():
        return execute(
            "INSERT INTO users(name,email,password_hash,created_at) VALUES(?,?,?,?)",
            (name, email, password_hash, now()),
        )
    row = cloud_client().table("users").insert({
        "name": name, "email": email, "password_hash": password_hash, "created_at": now()
    }).execute().data[0]
    return row["id"]

def find_user_by_email(email):
    if not cloud():
        return one("SELECT * FROM users WHERE email=?", (email,))
    rows = cloud_client().table("users").select("*").eq("email", email).limit(1).execute().data
    return rows[0] if rows else None

def get_user(user_id):
    if not cloud():
        return one("SELECT id,name,email,created_at FROM users WHERE id=?", (user_id,))
    rows = cloud_client().table("users").select("id,name,email,created_at").eq("id", user_id).limit(1).execute().data
    return rows[0] if rows else None

def upsert_profile(user_id, data):
    values = {
        "user_id": user_id,
        "age": data.get("age"),
        "height_cm": data.get("height_cm"),
        "weight_kg": data.get("weight_kg"),
        "activity_level": data.get("activity_level"),
        "dietary_preference": data.get("dietary_preference"),
        "goal": data.get("goal"),
        "allergies": data.get("allergies", ""),
        "updated_at": now(),
    }
    if not cloud():
        existing = one("SELECT id FROM profiles WHERE user_id=?", (user_id,))
        if existing:
            execute(
                """UPDATE profiles SET age=?,height_cm=?,weight_kg=?,activity_level=?,
                   dietary_preference=?,goal=?,allergies=?,updated_at=? WHERE user_id=?""",
                (values["age"], values["height_cm"], values["weight_kg"],
                 values["activity_level"], values["dietary_preference"], values["goal"],
                 values["allergies"], values["updated_at"], user_id),
            )
        else:
            execute(
                """INSERT INTO profiles(user_id,age,height_cm,weight_kg,activity_level,
                   dietary_preference,goal,allergies,created_at,updated_at)
                   VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (user_id, values["age"], values["height_cm"], values["weight_kg"],
                 values["activity_level"], values["dietary_preference"], values["goal"],
                 values["allergies"], now(), values["updated_at"]),
            )
        return get_profile(user_id)

    values["created_at"] = now()
    client = cloud_client()
    existing = client.table("profiles").select("user_id").eq("user_id", user_id).limit(1).execute().data
    if existing:
        client.table("profiles").update(values).eq("user_id", user_id).execute()
    else:
        client.table("profiles").insert(values).execute()
    return get_profile(user_id)

def get_profile(user_id):
    if not cloud():
        return one("SELECT * FROM profiles WHERE user_id=?", (user_id,))
    rows = cloud_client().table("profiles").select("*").eq("user_id", user_id).limit(1).execute().data
    return rows[0] if rows else None

def create_plan(user_id, plan):
    values = {
        "user_id": user_id,
        "breakfast": plan["breakfast"],
        "lunch": plan["lunch"],
        "snack": plan["snack"],
        "dinner": plan["dinner"],
        "nutrition_summary": plan["nutrition_summary"],
        "created_at": now(),
    }
    if not cloud():
        return execute(
            """INSERT INTO diet_plans(user_id,breakfast,lunch,snack,dinner,
               nutrition_summary,created_at) VALUES(?,?,?,?,?,?,?)""",
            tuple(values[k] for k in ["user_id","breakfast","lunch","snack","dinner","nutrition_summary","created_at"]),
        )
    row = cloud_client().table("diet_plans").insert(values).execute().data[0]
    return row["id"]

def get_plans(user_id):
    if not cloud():
        return all_rows("SELECT * FROM diet_plans WHERE user_id=? ORDER BY id DESC", (user_id,))
    return cloud_client().table("diet_plans").select("*").eq("user_id", user_id).order("id", desc=True).execute().data

def get_plan(user_id, plan_id):
    if not cloud():
        return one("SELECT * FROM diet_plans WHERE id=? AND user_id=?", (plan_id, user_id))
    rows = cloud_client().table("diet_plans").select("*").eq("id", plan_id).eq("user_id", user_id).limit(1).execute().data
    return rows[0] if rows else None

def delete_plan(user_id, plan_id):
    if not cloud():
        from backend.db import connect
        with connect() as conn:
            cur = conn.execute("DELETE FROM diet_plans WHERE id=? AND user_id=?", (plan_id, user_id))
            conn.commit()
            return cur.rowcount > 0
    result = cloud_client().table("diet_plans").delete().eq("id", plan_id).eq("user_id", user_id).execute()
    return bool(result.data)

def create_file_record(user_id, filename, storage_path):
    if not cloud():
        return execute(
            "INSERT INTO user_files(user_id,filename,storage_path,uploaded_at) VALUES(?,?,?,?)",
            (user_id, filename, storage_path, now()),
        )
    row = cloud_client().table("user_files").insert({
        "user_id": user_id, "filename": filename,
        "storage_path": storage_path, "uploaded_at": now()
    }).execute().data[0]
    return row["id"]

def get_files(user_id):
    if not cloud():
        return all_rows("SELECT * FROM user_files WHERE user_id=? ORDER BY id DESC", (user_id,))
    return cloud_client().table("user_files").select("*").eq("user_id", user_id).order("id", desc=True).execute().data

def get_file(user_id, file_id):
    if not cloud():
        return one("SELECT * FROM user_files WHERE id=? AND user_id=?", (file_id, user_id))
    rows = cloud_client().table("user_files").select("*").eq("id", file_id).eq("user_id", user_id).limit(1).execute().data
    return rows[0] if rows else None

def delete_file(user_id, file_id):
    if not cloud():
        from backend.db import connect
        with connect() as conn:
            cur = conn.execute("DELETE FROM user_files WHERE id=? AND user_id=?", (file_id, user_id))
            conn.commit()
            return cur.rowcount > 0
    result = cloud_client().table("user_files").delete().eq("id", file_id).eq("user_id", user_id).execute()
    return bool(result.data)
