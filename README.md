# AI-Powered Personal Diet Planner with Cloud Storage

A student-focused cloud-computing project that demonstrates authentication, REST APIs, user-specific data, a cloud-database adapter, object storage, an AI-style recommendation engine with an optional API and local fallback, testing, deployment, security, and GitHub proof-of-work.

> **Important:** This application generates general educational/wellness examples using synthetic/demo data. It is not a medical or clinical nutrition system.

## 1. Overview

The application lets a demo user register, log in, create a profile, generate a general meal-plan example, save plans, upload optional files, and retrieve user-specific data.

### Workflow

User → Web UI → Authentication → REST API → Recommendation Engine → Database → Object Storage → Dashboard

## 2. Recommended implementation

This repository uses **Python Flask + HTML/CSS/JavaScript** because it is easier for a student to understand and run end-to-end than a multi-service React project.

- Frontend: HTML, CSS, vanilla JavaScript
- Backend: Flask REST API
- Local database: SQLite
- Optional cloud database: Supabase Postgres through the Supabase Python client
- Local storage: `storage/`
- Optional cloud object storage: Supabase Storage
- Authentication: JWT issued by the Flask backend
- AI: deterministic rule-based engine by default; optional AI-compatible HTTP API
- Tests: pytest
- Deployment: Render Web Service or AWS/Azure/GCP equivalent

## 3. Cloud concepts demonstrated

| Concept | Where it appears |
|---|---|
| Cloud computing | Deploy the Flask service to a cloud web service |
| SaaS | Browser-accessible application |
| PaaS | Render Web Service can host the Python application |
| IaaS | AWS/Azure/GCP VM/container is an optional advanced deployment |
| Cloud database | `DATABASE_MODE=supabase` |
| Object storage | `STORAGE_MODE=supabase` |
| Authentication | `/api/register`, `/api/login`, JWT |
| REST API | `/api/*` endpoints |
| Client-server | Browser calls Flask APIs |
| Serverless | Optional future split into functions |
| Scalability | Stateless API + managed DB/object storage architecture |
| Load balancing | Cloud platform/load balancer in front of multiple instances |
| API gateway | Optional managed gateway in advanced architecture |
| Environment variables | `.env.example` |
| Secrets management | Never commit `.env` |
| Logging | Python logging |
| Monitoring | Cloud logs + health endpoint |
| Deployment | Render instructions |
| CI/CD | GitHub-triggered cloud deploy |

## 4. Technology options

### Option A — Beginner
HTML/CSS/JS + Flask + SQLite + local storage simulation.

- Difficulty: low
- Cost: local/free
- Best for understanding fundamentals
- Cloud concepts: REST, client-server, deployment, storage simulation
- Output: fully local demo

### Option B — Recommended
HTML/CSS/JS + Flask + JWT + SQLite locally + Supabase Postgres/Storage in cloud + rule-based AI fallback.

- Difficulty: medium
- Cost: suitable for a student prototype using free tiers where available
- Cloud concepts: authentication concepts, managed database, object storage, environment variables, deployment
- Output: strong end-to-end proof of work

### Option C — Advanced
React/Next.js + FastAPI + managed cloud database + object storage + managed authentication + serverless functions/API gateway + monitoring.

- Difficulty: high
- Cost: depends on provider and usage
- Cloud concepts: microservices/serverless, autoscaling, gateways, managed services
- Output: portfolio-grade architecture, but more moving parts

**Recommendation:** build Option B first, then add a React/FastAPI frontend only if the core system is already working.

## 5. Architecture

```text
                    ┌──────────────────────┐
                    │      Web Browser     │
                    │ HTML/CSS/JavaScript  │
                    └──────────┬───────────┘
                               │ HTTPS
                               ▼
                    ┌──────────────────────┐
                    │     Flask REST API   │
                    │ Auth + Validation    │
                    └───────┬───────┬──────┘
                            │       │
                ┌───────────┘       └──────────────┐
                ▼                                  ▼
       ┌────────────────┐                  ┌─────────────────┐
       │ Diet Engine    │                  │ Storage Service │
       │ Rules / AI API │                  │ Local/Supabase  │
       └───────┬────────┘                  └─────────────────┘
               │
               ▼
       ┌────────────────┐
       │ DB Service      │
       │ SQLite/Supabase │
       └────────────────┘
```

## 6. Data flow

1. User registers.
2. Backend validates the request and hashes the password.
3. User logs in and receives a JWT.
4. Browser stores the token for the demo session.
5. Protected endpoints require the JWT.
6. Profile data is saved against the authenticated user's ID.
7. `/api/generate-plan` sends structured preferences to the diet engine.
8. The engine first attempts the optional AI API when configured.
9. If the AI API is unavailable, the local rule-based engine generates the plan.
10. Saved plans are associated with the authenticated user's ID.
11. Uploaded files are stored locally or in Supabase Storage.
12. The dashboard retrieves only the current user's records.

## 7. Database design

### users

- `id` — primary key
- `name`
- `email` — unique
- `password_hash`
- `created_at`

### profiles

- `id` — primary key
- `user_id` — foreign key to users
- `age`
- `height_cm`
- `weight_kg`
- `activity_level`
- `dietary_preference`
- `goal`
- `allergies`
- `created_at`
- `updated_at`

### diet_plans

- `id` — primary key
- `user_id` — foreign key
- `breakfast`
- `lunch`
- `snack`
- `dinner`
- `nutrition_summary`
- `created_at`

### user_files

- `id` — primary key
- `user_id` — foreign key
- `filename`
- `storage_path`
- `uploaded_at`

## 8. Local setup

### Windows PowerShell

```powershell
git clone <YOUR-REPOSITORY-URL>
cd AI-Powered-Personal-Diet-Planner-Cloud

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

Copy-Item .env.example .env

python backend/app.py
```

Open:

```text
http://127.0.0.1:5000
```

### macOS/Linux

```bash
git clone <YOUR-REPOSITORY-URL>
cd AI-Powered-Personal-Diet-Planner-Cloud

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

python backend/app.py
```

## 9. Environment variables

Copy `.env.example` to `.env`.

The application defaults to local mode, so no paid service is required.

```text
SECRET_KEY=change-this-for-real-deployment
DATABASE_MODE=sqlite
SQLITE_PATH=instance/diet_planner.db
STORAGE_MODE=local
UPLOAD_FOLDER=storage
MAX_CONTENT_LENGTH_MB=5

SUPABASE_URL=
SUPABASE_KEY=
SUPABASE_SERVICE_KEY=
SUPABASE_BUCKET=diet-plans

AI_API_URL=
AI_API_KEY=
AI_MODEL=
```

Do not commit `.env`.

## 10. API endpoints

| Method | Endpoint | Auth |
|---|---|---|
| GET | `/api/health` | No |
| POST | `/api/register` | No |
| POST | `/api/login` | No |
| GET | `/api/profile` | Yes |
| PUT | `/api/profile` | Yes |
| POST | `/api/generate-plan` | Yes |
| GET | `/api/plans` | Yes |
| GET | `/api/plans/<id>` | Yes |
| DELETE | `/api/plans/<id>` | Yes |
| POST | `/api/upload` | Yes |
| GET | `/api/files` | Yes |
| DELETE | `/api/files/<id>` | Yes |

## 11. Testing

Run:

```bash
pytest -q
```

The test suite covers registration, duplicate email, login, profile, protected endpoints, plan generation, user isolation, file upload, and logout/token invalidation behavior.

## 12. Security basics

- Passwords are hashed with Werkzeug.
- JWT secrets come from environment variables.
- User-owned records are filtered by authenticated user ID.
- Uploads have a size limit and filename sanitization.
- CORS is restricted by `CORS_ORIGINS`.
- `.env` and local databases are ignored by Git.
- Production should use HTTPS.
- For a real deployment, use a managed secret store and stronger token/session lifecycle controls.
- Never place service-role cloud keys in browser JavaScript.

## 13. Deployment

### Render

Create a new Web Service connected to this GitHub repository.

Build command:

```text
pip install -r requirements.txt
```

Start command:

```text
gunicorn backend.app:app
```

Add environment variables from `.env.example`.

For a real cloud database, use Supabase or another managed Postgres service rather than SQLite. Free cloud services can have sleep, storage, bandwidth, and lifecycle limitations, so this project should be presented as a student prototype rather than a production healthcare service.

### AWS/Azure/GCP advanced architecture

Use:

- Managed compute/container service for Flask
- Managed Postgres
- Object storage bucket
- Managed identity/secrets
- HTTPS load balancer
- Monitoring/logging
- Optional serverless function for asynchronous AI generation

## 14. Cloud database vs object storage

**Database:** structured records such as user profiles and meal-plan metadata.

**Object storage:** files such as exported JSON/PDF files and demo meal images.

The project deliberately demonstrates both.

## 15. Scalability

### 10 users
A single Flask instance and managed database are sufficient for a student prototype.

### 1,000 users
Use multiple stateless API instances, a load balancer, managed Postgres, object storage, and caching where useful.

### 100,000 users
Separate frontend/API services, autoscaling, CDN, managed database with replicas/partitioning as appropriate, asynchronous queues for slow AI work, object storage, centralized logs, monitoring, rate limiting, and a gateway become important.

## 16. Screenshot checklist

Use these filenames:

1. `01-project-structure.png`
2. `02-architecture.png`
3. `03-registration.png`
4. `04-registration-success.png`
5. `05-login.png`
6. `06-profile.png`
7. `07-diet-preferences.png`
8. `08-plan-generation.png`
9. `09-generated-plan.png`
10. `10-plan-saved.png`
11. `11-database-record.png`
12. `12-storage-file.png`
13. `13-file-upload.png`
14. `14-saved-plans.png`
15. `15-dashboard.png`
16. `16-api-response.png`
17. `17-backend-terminal.png`
18. `18-test-results.png`
19. `19-cloud-dashboard.png`
20. `20-live-app.png`
21. `21-github-commits.png`
22. `22-github-repository.png`
23. `23-readme.png`

## 17. GitHub strategy

```bash
git init
git add .
git commit -m "Initialize cloud diet planner project"
git branch -M main
git remote add origin <YOUR-GITHUB-REPOSITORY-URL>
git push -u origin main
```

Suggested incremental commits:

```text
Create cloud application architecture
Add user authentication
Implement user profile management
Add AI diet recommendation engine
Implement diet plan REST API
Integrate cloud database
Add cloud object storage
Build user dashboard
Add AI fallback mechanism
Add application tests
Deploy application to cloud
Complete README and documentation
```

## 18. Disclaimer

This project uses synthetic/demo data and produces general educational/wellness examples. It does not diagnose conditions, prescribe treatment, or replace advice from a qualified healthcare professional.

## 19. Author

Add your name, college, course, GitHub URL, and LinkedIn URL here.
