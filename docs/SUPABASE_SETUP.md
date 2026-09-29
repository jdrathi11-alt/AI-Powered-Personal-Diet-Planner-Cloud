# Supabase Cloud Mode

1. Create a Supabase project.
2. Open the SQL Editor.
3. Run `cloud/supabase_schema.sql`.
4. Create a Storage bucket named `diet-plans`.
5. Copy the project URL and a server-side secret key into `.env`.
6. Set:
   - `DATABASE_MODE=supabase`
   - `STORAGE_MODE=supabase`
   - `SUPABASE_URL=...`
   - `SUPABASE_SERVICE_KEY=...`
   - `SUPABASE_BUCKET=diet-plans`
7. Deploy the Flask application.
8. Never put the service key in frontend JavaScript or GitHub.

The application still uses its own Flask JWT authentication in this student implementation. Supabase is used as the managed database and object-storage layer. For a more advanced version, migrate authentication to Supabase Auth and add Row Level Security policies based on `auth.uid()`.
