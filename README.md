# Apex Operations API — Junior DevOps Assessment

A small local API demonstrating containerization, CI checks, health/readiness, structured logs, a database dependency, and a reproducible rollback procedure.

## Assumptions and scope

- Local assessment environment only; no Apex production systems, real customer data, or paid cloud resources.
- Python 3.12, Flask, Docker Compose, PostgreSQL, pytest, Ruff, and GitHub Actions.
- `/health` is a liveness check. `/ready` checks PostgreSQL connectivity.
- The CI workflow tests, lints, and builds an image. It intentionally does not deploy.
- `scripts/intentional_failure.py` is a separate demonstration and is expected to exit with code 1. It is excluded from the normal passing CI suite.
- Gunicorn is used as the WSGI server for this local demo. Production deployment would require additional hardening and configuration.

## Prerequisites

- Docker Engine / Docker Desktop with Compose v2
- Python 3.12+ and Git for local tests
- GitHub account for hosted CI evidence

## Setup

```bash
cp .env.example .env
```

Edit `.env` and replace the example password with a strong local-only password. Do not commit `.env`.

Export the password into the shell used to run Compose:

```bash
set -a
source .env
set +a
```

Run the checks locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
ruff check app.py tests
pytest -q
```

Build and start the local stack:

```bash
docker compose up --build -d
docker compose ps
curl -i http://localhost:5000/
curl -i http://localhost:5000/health
curl -i http://localhost:5000/ready
curl -i http://localhost:5000/metrics
docker compose logs --tail=100 api
```

Stop the stack (the PostgreSQL volume remains):

```bash
docker compose down
```

To delete the database volume too (destructive):

```bash
docker compose down -v
```

## Six automated checks

The standard suite has six checks in `tests/test_app.py`; five cover the basic endpoints and version/metrics behavior, and two readiness checks cover database success/failure. (The suite currently contains six test functions; count actual test results when running it.)

Demonstrate an intentional failure separately:

```bash
python scripts/intentional_failure.py
echo $?
```

Expected result: exit code `1`. This is not a product defect; it is a controlled demonstration that a failing check can be captured without making the normal CI pipeline permanently red.

## Versioned image, release and rollback

Build a first version and save its tag:

```bash
export IMAGE_TAG=v1
docker compose build api
docker image inspect apex-operations-api:v1
```

Start that version:

```bash
docker compose up -d
curl -s http://localhost:5000/
```

For a new release, build a different tag (for example `v2`) and update the running service:

```bash
export IMAGE_TAG=v2
docker compose build api
docker compose up -d --no-build api
curl -s http://localhost:5000/
```

Rollback to the previous image tag:

```bash
export IMAGE_TAG=v1
docker compose up -d --no-build api
curl -s http://localhost:5000/
```

Capture evidence before and after rollback. Use actual image tags that exist locally. The app's response includes its version tag.

## Incident investigation exercise

A safe local exercise is to stop the database container and inspect readiness:

```bash
docker compose stop db
curl -i http://localhost:5000/ready
docker compose logs --tail=100 api
docker compose start db
curl -i http://localhost:5000/ready
```

Expected behavior: readiness returns HTTP 503 while the database is unavailable and returns HTTP 200 after recovery. Record the actual outputs and timestamps; do not claim results until you have run the commands.

## Security and operations notes

- Secrets: `.env` is git-ignored. Never put real credentials in source code, screenshots, or GitHub.
- Least privilege: the API container runs as UID 10001, has a read-only root filesystem, and uses a temporary filesystem for `/tmp`.
- Image/dependency scanning: add a scanner such as Trivy or `pip-audit` to CI; record the actual results and any limitations.
- Metrics/alerts proposal: scrape `/metrics`; alert on sustained readiness failures, elevated HTTP 5xx responses, and high restart counts. The included metrics endpoint is intentionally minimal.
- Cost-aware cloud path: use a small managed container or VM deployment, managed database only if needed, budget alerts, least-privilege IAM, logs retention limits, and shut down non-production resources when unused.

## Runbook

### Deploy
1. Confirm `.env` exists and `DB_PASSWORD` is set.
2. Run `docker compose build api`.
3. Run `docker compose up -d`.
4. Verify `docker compose ps`, `/health`, and `/ready`.
5. Check logs if any check fails.

### Rollback
1. Identify the previously known-good image tag.
2. Confirm it exists using `docker image inspect apex-operations-api:<tag>`.
3. Set `IMAGE_TAG` to that tag and run `docker compose up -d --no-build api`.
4. Verify the root endpoint version, health, and readiness.
5. Save before/after evidence.

### Incident response
1. Confirm the symptom with `/health` and `/ready`.
2. Inspect `docker compose ps` and `docker compose logs --tail=100 api db`.
3. Identify whether the API process or database dependency is failing.
4. Restore the dependency or roll back the application image.
5. Verify recovery and document timeline, cause, fix, and prevention.

## Evidence checklist

Save genuine screenshots/logs under `evidence/`:
- Docker build and running containers
- `/health`, `/ready`, and `/metrics`
- GitHub Actions successful run
- Passing test output and the separate intentional-failure output
- Version before rollback and after rollback
- Database outage investigation and recovery

## AI-use disclosure (edit to match what you actually did)

> I used ChatGPT to help interpret the assessment, propose a project structure, explain code and commands, and draft documentation. I reviewed, executed, and validated the submitted work myself. Any changes and actual test/deployment outcomes are documented in the repository. (Edit this statement so it accurately reflects your actual use and verification.)

## Decision memo (starter; revise after testing)

- Chosen stack: Flask + PostgreSQL + Docker Compose + GitHub Actions.
- Trade-off: small local reproducible scope rather than a paid cloud deployment.
- Release safety: version-tagged images and an explicit rollback to a previously built image.
- Limitations: minimal metrics, local-only deployment, and no production WSGI server or external alerting system.
- Next improvements: add dependency/image scanning to CI, stronger integration tests, production server, and deploy approval gates.
