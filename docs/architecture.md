# Architecture

```text
Developer commit
      |
      v
GitHub Actions
  |-- Ruff lint
  |-- pytest automated checks
  |-- Docker image build
      |
      v
Local Docker Compose
  |-----------------------|
  v                       v
Flask API              PostgreSQL
  |                       |
  |-- /health              |-- persistent named volume
  |-- /ready --------------|
  |-- /metrics
  |-- structured JSON logs
```

CI fails on lint, test, or image-build failure. The workflow does not deploy automatically.
