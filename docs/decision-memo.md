# Technical Decision Memo

## Context
This project demonstrates a containerized API, database dependency, automated CI, local deployment, and rollback without production access or paid cloud resources.

## Technical Decisions
1. Flask is used to implement the API.
2. Gunicorn serves the application.
3. Docker packages the application and its dependencies.
4. Docker Compose runs the API and PostgreSQL locally.
5. Health and readiness endpoints distinguish API health from database availability.
6. Versioned image tags such as v1 and v2 support deployment and rollback.
7. GitHub Actions runs lint, tests, and Docker image build.
8. Environment variables provide database configuration.

## Trade-offs
- This is a local assessment environment, not a production deployment.
- PostgreSQL runs as a single container.
- Local image tags are not a replacement for a remote registry.
- Production monitoring and vulnerability scanning are future improvements unless separately implemented and tested.

## Future Improvements
- Add dependency and container image vulnerability scanning.
- Publish immutable images to a secure registry.
- Use managed database and secrets services.
- Add production monitoring, alerting, and budget controls.
