#!/usr/bin/env bash
set -euo pipefail
: "${DB_PASSWORD:?Set DB_PASSWORD before deploying}"
export IMAGE_TAG="${IMAGE_TAG:-local}"
docker compose build api
docker compose up -d
docker compose ps
