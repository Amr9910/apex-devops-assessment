# Security and Observability

## Implemented Controls
- Application container is configured to run as a non-root user.
- API container uses a read-only root filesystem and temporary storage.
- Database credentials are provided through environment variables.
- The local .env file must never be committed.
- PostgreSQL is not exposed on a host port.
- Docker Compose includes API and database health checks.

## Health Checks
- GET /health: checks API health.
- GET /ready: checks database readiness.

## Log Investigation
Inspect API logs:
    docker compose logs --tail=100 api

Inspect database logs:
    docker compose logs --tail=100 db

## Metrics and Alerting Proposal
For a production environment, monitor:
- HTTP request count.
- Request latency.
- HTTP 5xx error rate.
- API availability.
- Database availability.

Proposed alerts include sustained API downtime, elevated server errors, high latency, and database outages. Thresholds should be based on observed workload.

## Vulnerability Scanning
Dependency and container image scanning are recommended CI improvements. No scan is claimed as completed unless it has actually been executed and evidenced.

## Least Privilege and Secrets
Use a dedicated database account with only the permissions required by the application. For cloud deployment, use a managed secrets service or workload identity. Rotate credentials and restrict deployment permissions.
