# REST API Reference

All protected endpoints require:

```text
Authorization: Bearer <JWT>
```

## POST /api/register

```json
{
  "name": "Demo User",
  "email": "demo@example.com",
  "password": "password123"
}
```

## POST /api/login

Returns a JWT.

## GET /api/profile

Returns the authenticated user and profile.

## PUT /api/profile

Stores demo profile preferences.

## POST /api/generate-plan

Generates a plan using the optional AI API or local fallback.

## GET /api/plans

Returns plans belonging to the authenticated user.

## GET /api/plans/<id>

Returns one plan belonging to the authenticated user.

## POST /api/plans

Stores the generated plan.

## DELETE /api/plans/<id>

Deletes a plan owned by the authenticated user.

## POST /api/upload

Multipart field: `file`.

## GET /api/files

Returns uploaded file records belonging to the authenticated user.

## DELETE /api/files/<id>

Deletes a file owned by the authenticated user.
