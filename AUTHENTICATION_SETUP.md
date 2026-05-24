# GitHub Authentication Setup & Push Instructions

## 🔐 Choose Your Authentication Method

You need to authenticate with GitHub to push. Choose one of the methods below:

---

## Method 1: Personal Access Token (PAT) ⭐ RECOMMENDED

### Step 1: Create a Personal Access Token on GitHub

1. Go to: https://github.com/settings/tokens/new
2. Login if needed
3. Fill in the form:
   - **Token name:** `Git-Exercises-Push`
   - **Expiration:** 30 days (or your preference)
   - **Scopes (check these boxes):**
     - ✅ `repo` (full control of repositories)
     - ✅ `workflow` (update GitHub Action workflows)
     - ✅ `write:packages` (write packages)

4. Click "Generate token"
5. **IMPORTANT:** Copy the token immediately (you won't see it again!)
   - Example: `ghp_1234567890abcdefghijklmnopqrstuvwxyz`

### Step 2: Configure Git to Use the Token

```bash
cd cloud-engineering-challenge

# Option A: Store credentials in Git credential helper (recommended)
git config --global credential.helper store

# Try to push (will prompt for credentials)
git push origin main

# When prompted:
#   Username: A96-45
#   Password: <paste your PAT here>

# Git will remember the credentials for future pushes
```

```bash
# Option B: Use token in URL directly (less secure, but works)
git remote set-url origin https://A96-45:<YOUR_PAT>@github.com/A96-45/cloud-engineering-challenge.git

# Then push normally
git push --all origin
```

### Step 3: Push All Branches

```bash
# Push all branches at once
git push --all origin

# Or push individually
git push origin main
git push origin develop
git push origin exercise/4-team-collaboration
# ... etc
```

---

## Method 2: GitHub CLI (Easiest if Installed)

### Prerequisites
- Install GitHub CLI: https://cli.github.com/
  - macOS: `brew install gh`
  - Linux: https://cli.github.com/
  - Windows: `scoop install gh`

### Steps

```bash
# 1. Authenticate
cd cloud-engineering-challenge
gh auth login

# Follow prompts:
#   - Choose: GitHub.com
#   - Choose: HTTPS (recommended)
#   - Choose: Authenticate with a web browser
#   - Follow browser prompt to authorize

# 2. Verify authentication worked
gh auth status

# 3. Push all branches
git push --all origin
```

---

## Method 3: SSH Keys (Most Secure)

### Prerequisites
- SSH key pair generated on your machine

### Step 1: Generate SSH Key (if you don't have one)

```bash
# Generate a new SSH key
ssh-keygen -t ed25519 -C "kellymelchris350@gmail.com"

# Press Enter for default location
# Set a passphrase (or leave empty)

# Verify it was created
ls -la ~/.ssh/id_ed25519*
```

### Step 2: Add SSH Key to GitHub

1. Copy your public key:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. Go to: https://github.com/settings/keys
3. Click "New SSH key"
4. Paste your public key
5. Click "Add SSH key"

### Step 3: Change Git Remote to SSH

```bash
cd cloud-engineering-challenge

# Change from HTTPS to SSH
git remote set-url origin git@github.com:A96-45/cloud-engineering-challenge.git

# Verify the change
git remote -v
```

### Step 4: Push All Branches

```bash
# Test SSH connection first
ssh -T git@github.com

# Should show: "Hi A96-45! You've successfully authenticated..."

# Push all branches
git push --all origin
```

---

## Troubleshooting

### Problem: "No such device or address"

**Cause:** Network configuration issue in this environment

**Solution:** Use one of the authentication methods above to create a connection

### Problem: "Authentication failed"

**Cause:** Wrong credentials or token

**Solution:**
1. Verify token is still valid: https://github.com/settings/tokens
2. Check username is correct: A96-45
3. Clear old credentials: `git config --global --unset user.password`

### Problem: "Permission denied (publickey)"

**Cause:** SSH key not properly set up

**Solution:**
```bash
# Verify SSH key exists
ls -la ~/.ssh/

# Test SSH connection
ssh -T git@github.com
```

### Problem: "fatal: the remote end hung up unexpectedly"

**Cause:** Large push or network timeout

**Solution:**
```bash
# Increase buffer size
git config http.postBuffer 524288000

# Try pushing individual branches instead
git push origin main
git push origin develop
# ... etc
```

---

## Quick Reference: Push Commands

### Push All Branches
```bash
git push --all origin
```

### Push Specific Branch
```bash
git push origin main
git push origin exercise/4-team-collaboration
```

### Push With Force (use with caution!)
```bash
# Force push (overwrites remote history)
git push origin main --force

# Safer alternative (won't overwrite if remote has new commits)
git push origin main --force-with-lease
```

### Verify Push Success
```bash
# List all branches on remote
git branch -r

# Fetch and check remote status
git fetch origin
git log --all --graph --oneline
```

---

## After Successful Push

### Verify on GitHub

1. Go to: https://github.com/A96-45/cloud-engineering-challenge
2. Check **Branches** tab to see all pushed branches
3. Check **Commits** to see all commits
4. Check specific branches by clicking their names

### Share Results

```
Repository: https://github.com/A96-45/cloud-engineering-challenge
Main branches: main, develop, release/v1.2
Exercise branches: exercise/*, feature/*, hotfix/*, bugfix/*
```

---

## Summary Table

| Method | Ease | Security | Best For |
|--------|------|----------|----------|
| PAT | ⭐⭐⭐⭐ | ⭐⭐⭐ | Quick setup |
| GitHub CLI | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Easiest overall |
| SSH | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Long-term use |

**Recommendation:** Start with **Personal Access Token** or **GitHub CLI** - both are straightforward and secure.

---
