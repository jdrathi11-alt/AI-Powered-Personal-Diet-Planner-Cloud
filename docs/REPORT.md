# Project Report — AI-Powered Personal Diet Planner with Cloud Storage

## Abstract

This project demonstrates a cloud-oriented web application that combines a REST backend, authentication, structured data storage, object storage, and an AI-style recommendation engine. The application is designed for educational use with synthetic/demo user information.

## Introduction

The goal is to show how cloud computing concepts can be applied to a practical full-stack application rather than treating cloud computing as only a hosting exercise.

## Problem Statement

Users may want to keep a reusable set of general meal-plan examples and access them through a browser. A cloud architecture makes centralized storage and multi-device access possible.

## Objectives

1. Implement user registration and login.
2. Protect user-specific application data.
3. Build REST APIs.
4. Generate general wellness meal-plan examples.
5. Demonstrate structured database storage.
6. Demonstrate object storage.
7. Deploy the application.
8. Document testing, security, and scalability.

## Existing System

A purely local application keeps data on one computer and does not demonstrate centralized cloud storage, cloud deployment, or scalable client-server architecture.

## Proposed System

The proposed system separates the browser UI, API layer, recommendation engine, database, and object storage. Local adapters make the application executable without paid cloud services.

## Cloud Computing Concepts

- SaaS: browser-accessible application.
- PaaS: managed web deployment.
- Cloud database: managed Postgres option.
- Object storage: managed file bucket option.
- Authentication: token-based protected API.
- REST: resource-oriented HTTP endpoints.
- Scalability: stateless application design.
- Availability: managed services and health monitoring.
- Elasticity: multiple application instances/autoscaling in advanced deployments.
- Secrets management: environment variables.
- Monitoring: application logs and health endpoint.
- CI/CD: Git-based deployment.

## System Architecture

Browser → Flask API → recommendation engine → database/object storage.

## Data Flow

Registration → login → profile → generate plan → save plan → upload file → dashboard retrieval.

## Database Design

The local implementation contains users, profiles, diet plans, and user files. Each resource has a user ID relationship so normal API operations remain user-specific.

## Cloud Storage Design

The local storage adapter writes files under a user-specific directory. The optional cloud adapter writes to a Supabase Storage bucket under `user-<id>/filename`.

## AI Recommendation Logic

The default engine is rule-based. It selects meal examples from a small predefined dataset based on dietary preference and incorporates general goal/activity labels. An optional HTTP AI API can be enabled through environment variables. If that API fails, the local engine is used.

## Authentication

Passwords are hashed. Login returns a JWT. Protected routes validate the JWT and use its user ID to scope database queries.

## API Design

The API provides registration, login, profile, plan, and file resources with JSON request/response bodies.

## Implementation

The frontend is intentionally small and readable. Flask serves both the UI and API, reducing deployment complexity for a student.

## Testing

Automated tests cover registration, duplicate registration, valid/invalid login, protected access, profile persistence, plan generation, and user isolation.

## Cloud Deployment

A PaaS web service can host the Flask API. A managed Postgres database and object storage service provide persistence outside the application filesystem.

## Security

Use HTTPS, secret environment variables, password hashing, authorization checks, file validation, upload limits, CORS restrictions, and least-privilege cloud credentials.

## Scalability

For larger traffic, place multiple stateless API instances behind a load balancer, use managed database services, object storage, caching/CDN, queues for slow work, and centralized monitoring.

## Results

The completed application demonstrates a working end-to-end flow from account creation to plan generation, persistence, and file storage.

## Advantages

- Beginner-friendly architecture.
- Local fallback.
- Optional cloud services.
- Clear separation of responsibilities.
- Demonstrates multiple cloud concepts.

## Limitations

- The local recommendation engine is intentionally simple.
- The application is not a clinical nutrition system.
- SQLite is not suitable for multi-instance production deployment.
- The cloud adapter requires provider configuration.

## Future Scope

- React frontend.
- FastAPI backend.
- Direct managed-auth integration.
- Row Level Security policies.
- Background AI jobs.
- PDF export.
- Analytics dashboard.
- Automated CI/CD pipeline.
- Centralized monitoring and alerts.

## Conclusion

The project provides a practical demonstration of cloud application development while remaining executable on a student laptop.

## Disclaimer

Generated content is for general educational/wellness demonstration only and is not medical advice.
