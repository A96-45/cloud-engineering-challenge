# CI/CD Pipeline Documentation

## Overview
This project uses GitHub Actions for continuous integration and deployment.

## Pipeline Stages

### 1. Lint (Code Quality)
- Runs on: Every push and PR
- Tools: flake8, black
- Status: Required to pass
- Time: ~30 seconds

### 2. Test (Unit Tests)
- Runs on: After lint passes
- Tools: pytest, coverage
- Status: Required to pass
- Time: ~45 seconds
- Coverage: Uploaded to Codecov

### 3. Build (Docker)
- Runs on: Successful push to main/develop
- Action: Build and push Docker image
- Registry: GitHub Container Registry (ghcr.io)
- Tags: Branch name, commit SHA, semantic version

### 4. Deploy to Staging
- Runs on: Push to develop
- Target: Staging environment
- Approval: Automatic
- Status: Informational

### 5. Semantic Release
- Runs on: Push to main
- Action: Create release tag
- Version: Semantic versioning (major.minor.patch)
- Status: Automatic release creation

## Workflow Triggers

```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  workflow_dispatch:  # Manual trigger
```

## Required Status Checks

Before merging a PR, the following must pass:
- ✅ Lint (flake8, black)
- ✅ Test (pytest with 80%+ coverage)
- ✅ Build (Docker image)

## Deployment Strategy

### Development Flow
```
feature/* → push → Lint ✅ → Test ✅ → Create PR
   ↓
Code Review & Approval
   ↓
Merge to develop → Lint ✅ → Test ✅ → Build 🐳 → Deploy Staging 🚀
```

### Release Flow
```
develop → (merge & tag) → main → Lint ✅ → Test ✅ → Build 🐳 → Release 📦
```

## Local Testing

Before pushing, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run linting
flake8 app/ tests/
black --check app/ tests/

# Run tests
pytest tests/ -v --cov=app

# Build Docker image
docker build -t cloud-optimizer:local .
docker run -p 5000:5000 cloud-optimizer:local
```

## Rollback Procedure

If deployment fails:

```bash
# Deploy previous stable version
kubectl rollout undo deployment/cloud-optimizer

# Or use docker
docker run -p 5000:5000 ghcr.io/A96-45/cloud-engineering-challenge:v1.0.0
```

## Monitoring

View pipeline status:
- GitHub Actions: https://github.com/A96-45/cloud-engineering-challenge/actions
- Docker Registry: ghcr.io
- Deployment metrics: (varies by platform)

## Configuration Files

- `Dockerfile` - Multi-stage Docker build
- `requirements.txt` - Python dependencies
- `.github/workflows/ci-cd.yml` - GitHub Actions workflow
- `tests/test_app.py` - Test suite
