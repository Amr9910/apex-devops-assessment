#!/usr/bin/env bash
set -euo pipefail
: "${DB_PASSWORD:?Set DB_PASSWORD before rollback}"
if [[ -z "${IMAGE_TAG:-}" ]]; then
  echo "Usage: DB_PASSWORD='...' IMAGE_TAG='<previous-image-tag>' ./scripts/rollback.sh"
  exit 2
fi
# The previous version must already exist locally as apex-operations-api:$IMAGE_TAG.
docker image inspect "apex-operations-api:${IMAGE_TAG}" >/dev/null
export IMAGE_TAG
docker compose up -d --no-build api
docker compose ps
