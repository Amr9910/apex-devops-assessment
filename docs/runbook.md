# Operations Runbook

## Prerequisites
- Docker Engine and Docker Compose.
- Local .env file created from .env.example.
- Never commit or share .env or its secrets.

## Deploy
Load environment variables:
    set -a
    source .env
    set +a

Deploy:
    IMAGE_TAG=v1 ./scripts/deploy.sh

## Verify
    docker compose ps
    curl -f http://localhost:5001/health
    curl -f http://localhost:5001/ready

## Upgrade
    IMAGE_TAG=v2 ./scripts/deploy.sh

## Rollback
    docker image ls apex-operations-api
    IMAGE_TAG=v1 ./scripts/rollback.sh

## Troubleshooting
- API logs: docker compose logs --tail=100 api
- Database logs: docker compose logs --tail=100 db
- Check database health if readiness fails.
- Check port 5001 if the API cannot start.

## Data safety
PostgreSQL uses the named volume postgres_data.
Never use docker compose down -v during normal rollback because it deletes the database volume.

## CI
GitHub Actions runs lint, tests, and image build. Production deployment is not configured. Deployment here is a manual local operation after successful CI.
