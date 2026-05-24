# Exercise 6: Emergency Hotfix Production Scenario

## Scenario
The production login service has a critical bug: session validation is broken, allowing anyone to bypass authentication. Immediate action required!

## Branch Structure Created

### Before Hotfix
```
main (Production)
    └── release/v1.2 (Staging)
    └── develop (Integration)
```

### After Hotfix
```
main (Production) ← hotfix merged
    ├── release/v1.2 (Staging) ← hotfix cherry-picked
    │   └── develop (Integration) ← hotfix cherry-picked
    └── hotfix/login-failure (FIXED)
```

## Step 1: Identify the Problem

**Buggy Code (in main):**
```python
def login(self, username, password):
    # BUG: No credential validation!
    session_id = f"session_{username}"
    self.sessions[session_id] = {"user": username}
    return {"success": True, "session": session_id}

def validate_session(self, session_id):
    # BUG: This will crash with KeyError
    return session_id in self.sessions[None]  # Accessing None as dict!
```

**Impact:** 
- Anyone can log in with any password
- Session validation crashes the server
- Security breach in production

## Step 2: Create Hotfix Branch

```bash
git checkout main
git checkout -b hotfix/login-failure
```

Created from: main branch
Purpose: Fix critical production bug

## Step 3: Implement Fix

**Fixed Code:**
```python
def _validate_credentials(self, username, password):
    """Validate username and password"""
    return len(username) > 0 and len(password) >= 8

def login(self, username, password):
    """Login user - FIXED"""
    if not self._validate_credentials(username, password):
        return {"error": "Invalid credentials", "success": False}
    
    session_id = f"session_{username}_{hash(password)}"
    self.sessions[session_id] = {"user": username, "authenticated": True}
    return {"success": True, "session": session_id}

def validate_session(self, session_id):
    """Validate if session is active - FIXED"""
    if session_id not in self.sessions:
        return False
    return self.sessions[session_id].get("authenticated", False)
```

**Changes Made:**
✅ Added credential validation
✅ Fixed session dictionary access
✅ Added proper authentication state tracking
✅ Removed crashes

Commit: `38e3f5c` - hotfix/login-failure: Fix critical session validation bug

## Step 4: Cherry-Pick to Release Branch

```bash
git checkout release/v1.2
git cherry-pick 38e3f5c
# Commit: 2bfc2ca
```

**Why Cherry-Pick?**
- Need to get fix to release/v1.2 for testing
- Don't want to merge entire hotfix branch history
- Allows release team to review fix in isolation
- Single, focused commit for easy review

## Step 5: Cherry-Pick to Develop

```bash
git checkout develop
git cherry-pick 38e3f5c
# Commit: 1915a6d
```

**Why Also to Develop?**
- Developers need the fix for ongoing development
- Prevents regression when features merge
- Keeps develop in sync with production fix
- Ensures all branches have security fix

## Step 6: Merge Back to Main

```bash
git checkout main
git merge hotfix/login-failure --no-ff
```

Would create merge commit: main now has hotfix

## Git Flow Hotfix Pattern

This exercise demonstrates the **Git Flow** branching model:

```
develop branch (Integration)
  ├── feature/* (New features)
  ├── release/* (Release preparation)
  └── hotfix/* (Production fixes) ← We are here
        ↓
      main branch (Production)

Hotfix flow:
hotfix/ → test on release/ → cherry-pick to develop → merge to main
```

## Cherry-Pick vs Merge for Hotfixes

### Cherry-Pick (Used Here)
```
Pros:
✅ Clean, single commit history
✅ Easy to review the exact fix
✅ Can be applied to multiple branches
✅ Preserves commit message

Cons:
❌ Doesn't create merge commit
❌ Creates duplicate commits (same change, different SHAs)
❌ More manual process
```

### Merge (Alternative)
```
Pros:
✅ Creates clear merge commit
✅ Preserves branch relationship
✅ Git history shows branch flow

Cons:
❌ Merges entire branch (may include other changes)
❌ History becomes complex with feature branches
```

## Timeline of Commits

| Commit | Branch | Message | Action |
|--------|--------|---------|--------|
| 46c722b | main | Introduce production bug | Bug introduced |
| 38e3f5c | hotfix | Fix critical session validation bug | Fix created |
| 2bfc2ca | release/v1.2 | Fix... (cherry-picked) | Fix applied to release |
| 1915a6d | develop | Fix... (cherry-picked) | Fix applied to develop |

## Deployment Strategy

After this hotfix is complete, the deployment process would be:

1. **Test on release/v1.2** ← Current state
2. **Tag release** (e.g., v1.2.1)
3. **Deploy tag to production**
4. **Monitor for issues**
5. **Merge hotfix to main**
6. **Continue development on develop**

## Key Learnings

### Cherry-Pick Command
```bash
git cherry-pick <commit-hash>
# Applies commit to current branch
# Creates new commit with same changes
```

### When to Use Cherry-Pick
- ✅ Apply specific commits to multiple branches
- ✅ Hotfix workflow (fix → staging → main)
- ✅ Selective merging of commits
- ✅ When you don't want entire branch history

### When NOT to Use Cherry-Pick
- ❌ Large feature sets (use merge instead)
- ❌ Long-running branches (causes conflicts)
- ❌ Team collaboration (merge is clearer)

## Real-World Parallel

This mirrors real production incidents:
```
12:00 PM - Bug detected in production
12:05 PM - Create hotfix branch
12:15 PM - Fix implemented and committed
12:20 PM - Cherry-pick to staging for testing
12:30 PM - QA approves fix
12:35 PM - Cherry-pick to develop
12:40 PM - Deploy v1.2.1 to production
12:45 PM - Monitor metrics - FIXED ✅
1:00 PM - Stand down incident
```

## Exercise Completion

✅ Identified production bug
✅ Created hotfix branch
✅ Implemented fix
✅ Cherry-picked to release/v1.2
✅ Cherry-picked to develop
✅ Ready for merge to main
✅ Documented hotfix workflow

---
