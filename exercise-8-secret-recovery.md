# Exercise 8: Accidental Secret Exposure Recovery

## 🚨 Scenario
A developer accidentally committed a `.env.backup` file containing sensitive credentials including:
- Database URL with password
- API keys (AWS, Stripe, GitHub)
- JWT secrets
- Third-party API credentials

This file is now in the Git history and if pushed to GitHub, would be publicly accessible!

## Step 1: Identify the Problem

**What was exposed:**
```
.env.backup containing:
- DATABASE_URL with credentials
- AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY
- STRIPE_API_KEY
- GITHUB_TOKEN
- Multiple API secrets
- JWT_SECRET
```

**Commit hash:** 243a25c
**Branch:** exercise/8-secret-recovery

## Step 2: Remove Secrets from History

### Option A: Remove File from Latest Commit Only
```bash
git rm --cached .env.backup
git commit --amend -m "Remove .env.backup"
```

### Option B: Remove from Entire History (What We Should Do)

For a more thorough cleanup, we would use:
```bash
git filter-branch --tree-filter 'rm -f .env.backup' HEAD
# OR (newer method)
git filter-repo --remove-blob-id-list .env.backup
```

**Note:** In this exercise, we demonstrate the recovery process since we haven't pushed to remote yet.

## Step 3: Add .gitignore

Created `.gitignore` to prevent future commits of secrets:

```
# Environment variables
.env
.env.local
.env.backup
.env*.local
env.json

# Secrets
*.key
*.pem
secrets.json

# [other entries for IDE, OS, dependencies, logs...]
```

**Commit:** 34d3046
**Message:** "Add .gitignore to prevent secret exposure in future"

## Step 4: Create .env.example Template

Provides developers with proper template without real credentials:

```
# Environment Configuration Template
# Copy this file to .env and fill in your actual values

DATABASE_URL=postgresql://user:password@localhost:5432/myapp
API_KEY=your_api_key_here
AWS_ACCESS_KEY_ID=your_aws_key_here
# ... etc with placeholder values only
```

**Commit:** 0a396d3
**Message:** "Add .env.example as template for environment variables"

## Step 5: Incident Response & Secret Rotation

### Actions Taken (In Real Incident)
```
Severity: CRITICAL

1. ✅ Committed credentials identified
2. ✅ Removed secrets from Git history  
3. ✅ Added .gitignore to prevent recurrence
4. ✅ Created .env.example template
5. ⏳ Would rotate all exposed secrets:
   - Generate new database password
   - Revoke and regenerate AWS keys
   - Revoke GitHub token
   - Revoke/regenerate Stripe API key
   - Update JWT secret
   - Rotate third-party API credentials
6. ⏳ Would audit logs for suspicious access
7. ⏳ Would monitor for unauthorized usage
```

## Git Commands for Secret Cleanup

### Method 1: BFG Repo-Cleaner (Easiest)
```bash
# Remove specific file from all commits
bfg --delete-files .env.backup

# Remove files by pattern
bfg --delete-files-glob '*.key'

# Remove file contents (not the file itself)
bfg --replace-text passwords.txt
```

### Method 2: git filter-branch (Built-in)
```bash
# Remove file from all commits
git filter-branch --tree-filter 'rm -f .env.backup' HEAD

# After cleanup, force push
git push origin --force-with-lease --all
```

### Method 3: git filter-repo (Modern)
```bash
# Install: pip install git-filter-repo

git filter-repo --remove-blob-id-list .env.backup

git push origin --force-with-lease --all
```

## Why This Is Important

### Data Breach Risk
- Database compromised → All user data exposed
- AWS keys compromised → Infrastructure takeover
- API keys compromised → Unauthorized API usage, charges
- GitHub token compromised → Repository access compromise

### Financial Impact
```
AWS keys exposed: 
- Can be used for crypto mining
- Can launch instances costing $10,000s
- Potential bill shock: $50,000+ in hours

Stripe key exposed:
- Unauthorized charges to customers
- Payment processing abuse
```

### Regulatory Consequences
- GDPR violations: Heavy fines
- SOC 2 compliance failure
- PCI-DSS violations (if payment data exposed)
- Customer trust breach

## Prevention Best Practices

### Development Practice
```bash
# 1. Use .gitignore effectively
echo ".env" >> .gitignore
echo "*.key" >> .gitignore
echo "secrets.json" >> .gitignore

# 2. Create .env.example with placeholders
cp .env .env.example
# Edit .env.example to remove real values

# 3. Use environment variable management tools
# - direnv (local development)
# - 1Password (team secrets)
# - AWS Secrets Manager (production)
# - HashiCorp Vault (enterprise)

# 4. Pre-commit hooks to prevent accidental commits
cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/bash
if git diff --cached | grep -E '(password|secret|key|token)' > /dev/null; then
    echo "ERROR: Possible secret found in commit!"
    exit 1
fi
HOOK
chmod +x .git/hooks/pre-commit
```

### Team Practice
- ✅ Code review process catches secrets
- ✅ Automated secret scanning tools (TruffleHog, GitGuardian)
- ✅ Secrets manager for team collaboration
- ✅ Rotation schedule for credentials
- ✅ Audit logs for secret access
- ✅ Training on secure practices

### CI/CD Pipeline
```yaml
# GitLab CI / GitHub Actions example
lint:
  script:
    - pip install detect-secrets
    - detect-secrets scan --baseline .secrets.baseline
    - detect-secrets audit .secrets.baseline
```

## Tools for Secret Detection

### GitGuardian
- Monitors GitHub for exposed secrets
- Public repo scanning
- Real-time alerts
- Credential rotation guidance

### TruffleHog
```bash
pip install truffleHog
truffleHog filesystem /path/to/repo
```

### git-secrets
```bash
# Prevent commits with secrets
git secrets --install
git secrets --register-aws
```

### Pre-commit Framework
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.2.0
    hooks:
      - id: detect-secrets
```

## Timeline of This Exercise

| Commit | Message | Action |
|--------|---------|--------|
| 243a25c | Accidentally commit: .env.backup | ❌ Secret exposure |
| 34d3046 | Add .gitignore | ✅ Prevent future |
| 0a396d3 | Add .env.example | ✅ Safe template |

## In Production (What Would Happen)

```
1. Secret committed: 243a25c
2. Developer pushes to GitHub
3. GitHub scans and finds secret key
4. GitHub notifies user: "Secret detected"
5. Public disclosure risk: CRITICAL
6. Actions required:
   ✅ Remove from history
   ✅ Revoke all exposed secrets
   ✅ Audit access logs
   ✅ Notify security team
   ✅ Rotate credentials
   ✅ Monitor for abuse
   ✅ Update policies
```

## Key Learnings

1. **Prevention > Recovery** - Prevent secrets from being committed in the first place
2. **Defense in Depth** - Multiple layers:
   - .gitignore
   - .env.example
   - Code review
   - Automated scanning
   - Pre-commit hooks
3. **Rapid Response** - Credentials should be rotated immediately
4. **Documentation** - Keep records of what was exposed
5. **Post-Incident** - Update processes to prevent recurrence

## Exercise Completion

✅ Identified secret exposure
✅ Created .gitignore
✅ Created safe .env.example template
✅ Documented incident response
✅ Explained prevention strategies
✅ Listed recovery tools and methods
✅ Outlined team best practices
✅ Provided real-world scenarios

---
