# Exercise 9: Full CI/CD Git Workflow Project

## Project Overview
Complete cloud cost optimization dashboard with full CI/CD pipeline implementation using GitHub Actions.

## Repository Structure

```
cloud-engineering-challenge/
├── .github/
│   └── workflows/
│       └── ci-cd.yml              (GitHub Actions pipeline)
├── app/
│   └── app.py                     (Flask application)
├── tests/
│   └── test_app.py                (Pytest test suite)
├── Dockerfile                     (Multi-stage build)
├── requirements.txt               (Python dependencies)
├── README_CICD.md                 (Pipeline documentation)
└── exercise-9-cicd.md            (This file)
```

## Step 1: Create Flask Application

### Files Created
- `app/app.py` - Main Flask application
- `requirements.txt` - Project dependencies

### Endpoints Implemented
```python
GET /                    # Health check
GET /health              # Health status
GET /api/costs           # Cost data
```

### Error Handling
- 404: Not Found
- 500: Internal Server Error

**Commit:** 799abc4

## Step 2: Docker Containerization

### Multi-Stage Build Strategy

```dockerfile
Stage 1: base
  - Python 3.9 slim
  - Install build tools

Stage 2: dependencies
  - Install Python requirements

Stage 3: builder
  - Compile Python code

Stage 4: runtime
  - Final minimal image
  - Copy dependencies from stage 3
  - Only runtime, no build tools
```

### Benefits of Multi-Stage Build
- ✅ Smaller image size (~150MB vs 500MB+)
- ✅ Reduced attack surface (no build tools)
- ✅ Faster deployment
- ✅ Better security (fewer vulnerabilities)

**Commit:** 75f7cbf - Dockerfile
**Commit:** b2e3df0 - requirements.txt

## Step 3: Test Suite Implementation

### Unit Tests Created

```python
test_index()           # Test home endpoint
test_health_check()    # Test health check
test_get_costs()       # Test cost data
test_not_found()       # Test 404 handling
test_response_headers()# Test response format
```

### Test Metrics
- Tests: 5
- Coverage target: 80%+
- Framework: pytest
- Coverage tool: pytest-cov

**Commit:** 9f656af

## Step 4: GitHub Actions CI/CD Pipeline

### Pipeline Stages

#### Stage 1: Lint
```yaml
Tools: flake8, black
Runs: On push and PR
Status: Required for merge
Duration: ~30 seconds
```

Tasks:
- Syntax checking with flake8
- Code formatting validation with black
- Exit on critical errors (E9, F63, F7, F82)

#### Stage 2: Test
```yaml
Tools: pytest, pytest-cov
Runs: After lint passes
Status: Required for merge
Duration: ~45 seconds
```

Tasks:
- Run unit tests
- Generate coverage report
- Upload to Codecov

#### Stage 3: Build
```yaml
Tool: Docker buildx
Runs: After successful push to main/develop
Status: Required before deploy
Duration: ~90 seconds
```

Tasks:
- Build Docker image
- Generate tags (branch, sha, semver)
- Push to GitHub Container Registry (ghcr.io)

#### Stage 4: Deploy
```yaml
Target: Staging environment
Runs: After build on develop push
Status: Automatic
Duration: ~60 seconds
```

Tasks:
- Deploy to staging
- Run smoke tests
- Monitor health checks

#### Stage 5: Semantic Release
```yaml
Target: Production
Runs: After build on main push
Status: Automatic
Duration: ~30 seconds
```

Tasks:
- Create semantic version tag
- Generate release notes
- Publish release

**Commit:** a9440e1

## Step 5: Pipeline Configuration

### Triggers
```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  workflow_dispatch:  # Manual trigger
```

### Conditional Execution
```yaml
# Build only on successful push
if: github.event_name == 'push'

# Deploy staging only on develop
if: github.ref == 'refs/heads/develop'

# Release only on main
if: github.ref == 'refs/heads/main'
```

### Environment Variables
```yaml
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
```

### Secrets Required
```
GITHUB_TOKEN        # Auto-provided
DOCKER_REGISTRY_PAT # For registry push
DEPLOY_TOKEN        # For staging deployment
```

## Git Workflow with CI/CD

### Feature Development
```
1. Create feature branch
   git checkout -b feature/cost-analytics

2. Make changes and commits
   git add .
   git commit -m "Add cost analytics"

3. Push to remote
   git push origin feature/cost-analytics

4. Create Pull Request on GitHub
   - GitHub Actions runs lint + test
   - Status checks must pass
   - Code review required

5. Merge to develop
   - GitHub Actions runs lint + test
   - Builds Docker image
   - Deploys to staging
```

### Release Process
```
1. Create release branch
   git checkout -b release/v1.1.0

2. Update version numbers
   git add .
   git commit -m "Bump version to 1.1.0"

3. Merge to main
   - GitHub Actions runs full pipeline
   - Creates release tag
   - Pushes to production

4. Merge back to develop
   git checkout develop
   git merge release/v1.1.0
   git push origin develop
```

## Status Checks & Branch Protection

### Required Checks Before Merge
```
✅ lint (flake8, black)
✅ test (pytest + coverage)
✅ build (Docker image)
```

### Branch Protection Rules (Recommended)
```
1. Require pull request reviews before merging
2. Require status checks to pass
3. Require branches to be up to date
4. Dismiss stale PR approvals
5. Require conversation resolution
6. Require commits to be signed (optional)
```

## Monitoring & Troubleshooting

### View Pipeline Status
```bash
# Local
git log --oneline --graph

# GitHub
https://github.com/A96-45/cloud-engineering-challenge/actions
```

### Common Issues

**Issue: Lint fails**
```bash
# Fix formatting locally
black app/ tests/
git add .
git commit --amend
git push --force-with-lease
```

**Issue: Tests fail**
```bash
# Run tests locally
pytest tests/ -v

# Debug with more output
pytest tests/ -v -s --tb=long
```

**Issue: Docker build fails**
```bash
# Build locally
docker build -t test:local .

# Check for issues
docker run -it test:local bash
```

## Deployment Strategy

### Staging Deployment
- Target: develop branch
- Automatic: Yes
- Rollback: Manual or automated
- Testing: Smoke tests + manual QA

### Production Deployment
- Target: main branch
- Automatic: Release only
- Rollback: Via previous tag
- Testing: Pre-release staging validation

### Rollback Procedure
```bash
# Deploy previous version
git checkout v1.0.0
git push -f refs/tags/v1.0.0:refs/heads/main

# Or use container
docker pull ghcr.io/A96-45/...:v1.0.0
```

## Key Learnings

1. **Separation of Concerns** - Each stage has single responsibility
2. **Fast Feedback** - Developers know results in minutes
3. **Quality Gates** - Automated prevention of bad code
4. **Traceability** - Every build tied to specific commit
5. **Automation** - Removes manual, error-prone steps
6. **Repeatability** - Same process every time
7. **Documentation** - Pipeline behavior is clearly defined

## Real-World Enhancements

### Security
```yaml
- Secrets scanning (TruffleHog)
- Vulnerability scanning (Trivy)
- SAST (CodeQL)
- Container signing
```

### Performance
```yaml
- Cache Docker layers
- Parallel job execution
- Test sharding
- Build matrix for multiple versions
```

### Observability
```yaml
- Slack notifications
- GitHub release notes
- Deployment tracking
- Performance metrics
```

## Files Overview

| File | Purpose | Lines |
|------|---------|-------|
| Dockerfile | Container definition | 26 |
| requirements.txt | Dependencies | 9 |
| app/app.py | Application logic | 53 |
| tests/test_app.py | Unit tests | 46 |
| .github/workflows/ci-cd.yml | Pipeline definition | 137 |
| README_CICD.md | Pipeline docs | 60 |

## Exercise Completion

✅ Created Flask application with endpoints
✅ Implemented multi-stage Dockerfile
✅ Created comprehensive test suite
✅ Built GitHub Actions CI/CD pipeline
✅ Configured lint, test, build stages
✅ Implemented staging deployment
✅ Automatic semantic release
✅ Documented entire workflow
✅ Explained best practices

---
