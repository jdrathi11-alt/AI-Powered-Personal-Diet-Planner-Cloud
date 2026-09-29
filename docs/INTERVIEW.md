# Interview Preparation

## 1. Explain your project.
I built a cloud-oriented personal diet planning application for educational use. The browser communicates with a Flask REST API. The backend authenticates users, stores profiles and saved plans, generates a general wellness meal-plan example through a local rule-based engine or optional AI API, and stores uploaded files through a local or cloud object-storage adapter. The architecture is designed so the local version works without paid services while the cloud version can use managed database and storage services.

## 2. Why did you use a REST API?
It separates the client from the server and gives the application clear resource-oriented endpoints. It also makes it easier to replace the frontend later with React or a mobile client.

## 3. What is the difference between a cloud database and object storage?
A database stores structured records that the application queries and updates. Object storage is optimized for files such as images, exported documents, and other binary objects.

## 4. How did you protect user data?
The backend issues JWTs after login and protected routes extract the user ID from the token. Database queries include that user ID so one authenticated user cannot normally retrieve another user's records.

## 5. How does the AI component work?
The default implementation is deterministic and uses a small food dataset plus preference rules. An optional HTTP AI service can be configured. If the service is unavailable or returns an invalid response, the application falls back to the local engine.

## 6. Why is SQLite not enough for production scaling?
SQLite is a local file database. It is useful for development but becomes unsuitable when multiple application instances need concurrent shared state. A managed Postgres database provides centralized durable storage and better multi-instance behavior.

## 7. How would you scale to many users?
I would keep the API stateless, place multiple instances behind a load balancer, move persistent data to managed Postgres and object storage, add caching, rate limiting and queues for slow AI operations, and centralize monitoring.

## 8. How did you handle secrets?
Secrets are environment variables and `.env` is ignored by Git. Cloud service-role credentials must stay on the server and should be stored in a managed secret system in a production deployment.

## 9. What happens if the AI API fails?
The application catches request/response errors and uses the local rule-based fallback. This keeps the demo executable without a paid AI API.

## 10. What would you improve next?
I would add direct managed authentication with stronger session handling, Row Level Security, a React frontend, automated cloud deployment, centralized monitoring, asynchronous AI jobs, and a more formal cloud infrastructure configuration.
