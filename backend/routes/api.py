from flask import Blueprint, jsonify, request, g
from backend.security import hash_password, verify_password, create_token, require_auth
from backend import models
from backend.ai_engine.diet_engine import generate_plan
from backend.cloud.storage_service import save_file, delete_file

api = Blueprint("api", __name__, url_prefix="/api")

def clean_email(email):
    return (email or "").strip().lower()

@api.get("/health")
def health():
    return jsonify({"status": "ok", "service": "ai-diet-planner"})

@api.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = clean_email(data.get("email"))
    password = data.get("password") or ""

    if len(name) < 2:
        return jsonify({"error": "Name must contain at least 2 characters"}), 400
    if "@" not in email:
        return jsonify({"error": "Enter a valid email"}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400
    if models.find_user_by_email(email):
        return jsonify({"error": "Email already registered"}), 409

    user_id = models.create_user(name, email, hash_password(password))
    return jsonify({"message": "Registration successful", "user_id": user_id}), 201

@api.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = clean_email(data.get("email"))
    password = data.get("password") or ""
    user = models.find_user_by_email(email)

    if not user or not verify_password(password, user["password_hash"]):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({
        "token": create_token(user["id"]),
        "user": {"id": user["id"], "name": user["name"], "email": user["email"]}
    })

@api.get("/profile")
@require_auth
def profile():
    return jsonify({"user": models.get_user(g.user_id), "profile": models.get_profile(g.user_id)})

@api.put("/profile")
@require_auth
def update_profile():
    data = request.get_json(silent=True) or {}
    allowed = {
        "age", "height_cm", "weight_kg", "activity_level",
        "dietary_preference", "goal", "allergies"
    }
    clean = {k: data.get(k) for k in allowed}
    return jsonify({"profile": models.upsert_profile(g.user_id, clean)})

@api.post("/generate-plan")
@require_auth
def generate():
    profile = models.get_profile(g.user_id)
    if not profile:
        return jsonify({"error": "Complete your profile first"}), 400
    plan = generate_plan(profile)
    return jsonify({"plan": plan})

@api.get("/plans")
@require_auth
def plans():
    return jsonify({"plans": models.get_plans(g.user_id)})

@api.get("/plans/<int:plan_id>")
@require_auth
def get_plan(plan_id):
    plan = models.get_plan(g.user_id, plan_id)
    if not plan:
        return jsonify({"error": "Plan not found"}), 404
    return jsonify({"plan": plan})

@api.post("/plans")
@require_auth
def save_plan():
    data = request.get_json(silent=True) or {}
    required = ["breakfast", "lunch", "snack", "dinner", "nutrition_summary"]
    if any(not data.get(k) for k in required):
        return jsonify({"error": "Incomplete plan"}), 400
    plan_id = models.create_plan(g.user_id, data)
    return jsonify({"message": "Plan saved", "plan_id": plan_id}), 201

@api.delete("/plans/<int:plan_id>")
@require_auth
def delete_plan(plan_id):
    if not models.delete_plan(g.user_id, plan_id):
        return jsonify({"error": "Plan not found"}), 404
    return jsonify({"message": "Plan deleted"})

@api.post("/upload")
@require_auth
def upload():
    try:
        path = save_file(request.files.get("file"), g.user_id)
        file_id = models.create_file_record(
            g.user_id, request.files["file"].filename, path
        )
        return jsonify({"message": "File uploaded", "file_id": file_id, "storage_path": path}), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Storage service failed"}), 500

@api.get("/files")
@require_auth
def files():
    return jsonify({"files": models.get_files(g.user_id)})

@api.delete("/files/<int:file_id>")
@require_auth
def delete_uploaded_file(file_id):
    record = models.get_file(g.user_id, file_id)
    if not record:
        return jsonify({"error": "File not found"}), 404
    try:
        delete_file(record["storage_path"])
        models.delete_file(g.user_id, file_id)
        return jsonify({"message": "File deleted"})
    except Exception:
        return jsonify({"error": "Storage service failed"}), 500
