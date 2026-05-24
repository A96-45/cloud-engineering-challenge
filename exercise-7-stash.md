# Exercise 7: Stash and Context Switching Exercise

## Scenario
You are developing a payment system feature when an urgent database bug is reported. You need to:
1. Save your unfinished work
2. Fix the urgent bug
3. Return to your payment feature and continue

## Step 1: Unfinished Work on feature/payment-system

Started work on payment processing system with:
- `payment/payment-processor.py` - Main payment processing class
- `payment/payment-models.py` - Data models for transactions
- `payment/payment-api.py` - REST API endpoints (not yet committed)
- `README_PAYMENT.md` - Feature documentation (not yet committed)

**Status:** 2 commits made, 2 files in staging area waiting to be committed

```
Commit 95544e3: Start payment processor implementation
Commit 24fda1a: Add payment data models
WIP: payment-api.py and README_PAYMENT.md staged
```

## Step 2: Urgent Bug Notification

Database connection pool is leaking connections, causing production outages.

**Action:** Must stop work immediately and fix critical bug

## Step 3: Stash Work-in-Progress

```bash
git stash push -m "WIP: Payment system API endpoints and readme - interrupted for urgent bug"
```

**What happens:**
- All staged and modified files are saved to stash
- Working directory is cleaned
- You can now safely switch branches

```
Saved working directory and index state On feature/payment-system:
WIP: Payment system API endpoints and readme - interrupted for urgent bug

Stash List:
stash@{0}: On feature/payment-system: WIP: Payment system API endpoints and readme - interrupted for urgent bug
```

### Stash Details

**Files stashed:**
- README_PAYMENT.md
- payment/payment-api.py

**Branch:** feature/payment-system
**State:** Ready to switch to different branch

## Step 4: Switch Context to Fix Urgent Bug

```bash
git checkout main
git checkout -b bugfix/urgent-database-error
```

### Bugfix Implementation

Created `app/database-fix.py` with:
- Proper connection pool management
- Connection lifecycle tracking
- Release mechanism to prevent leaks

```python
class DatabasePool:
    def get_connection(self):
        """Get connection from pool"""
        # Connection management logic
        
    def release_connection(self, conn):
        """Release connection back to pool"""
        # Proper cleanup and reuse
```

### Bugfix Commits

```
Commit 7bb5c3d: Fix database connection pool leak
Commit b83d6de: Add bugfix documentation
```

**Time on bugfix:** 2 commits, quick turnaround ✅

## Step 5: Return to Original Work

```bash
git checkout feature/payment-system
```

**Status:** Back on original branch with previous commits intact

```
Commit 24fda1a: Add payment data models
Commit 95544e3: Start payment processor implementation
```

## Step 6: Apply Stashed Work

```bash
git stash pop
```

OR (if you want to inspect first):
```bash
git stash show -p      # Preview changes
git stash list         # List all stashes
git stash pop          # Apply and remove from stash
```

### Result

```
Changes to be committed:
  new file:   README_PAYMENT.md
  new file:   payment/payment-api.py
```

**Work restored:** All staged changes are back, ready to continue!

### Final Commit

```bash
git add payment/payment-api.py README_PAYMENT.md
git commit -m "feature/payment-system: Resume payment API and documentation"
```

## Git Stash Commands Reference

### Save Work
```bash
git stash                          # Stash with auto-generated message
git stash save "description"       # Stash with custom message
git stash push -m "message"        # Push to stash (newer syntax)
git stash push -u                  # Include untracked files
```

### View Stashes
```bash
git stash list                     # List all stashes
git stash show                     # Show latest stash changes
git stash show -p stash@{0}        # Show full diff of specific stash
```

### Apply Stashes
```bash
git stash pop                      # Apply and remove from stash
git stash apply                    # Apply but keep in stash
git stash apply stash@{2}          # Apply specific stash
```

### Manage Stashes
```bash
git stash drop                     # Delete latest stash
git stash drop stash@{2}           # Delete specific stash
git stash clear                    # Delete all stashes
```

### Create Branch from Stash
```bash
git stash branch new-branch-name   # Create branch with stash content
```

## When to Use Stash

### Perfect Use Cases
✅ Switching branches with uncommitted changes
✅ Interrupted by urgent bug fixes
✅ Context switching in busy day
✅ Experimental work you're not ready to commit
✅ Saving work before pulling from remote
✅ Quick save before rebasing

### When NOT to Use Stash
❌ Long-term storage (use branches instead)
❌ Permanent work (make commits instead)
❌ Team collaboration (use branches for sharing)
❌ As a workaround for merge conflicts (resolve conflicts)

## Common Stash Workflows

### Workflow 1: Quick Bug Fix
```
1. Working on feature/awesome
2. git stash                    (save work)
3. git checkout bugfix/urgent   (switch branches)
4. Fix bug and commit
5. git checkout feature/awesome (return)
6. git stash pop                (resume work)
```

### Workflow 2: Pull Latest Changes
```
1. Working with uncommitted changes
2. git stash                    (save work)
3. git pull origin develop      (fetch latest)
4. git stash pop                (resume with new base)
```

### Workflow 3: Wrong Branch Commit
```
1. Realized committed to wrong branch
2. git reset HEAD~1             (undo commit)
3. git stash                    (save changes)
4. git checkout correct-branch  (switch)
5. git stash pop                (apply there)
6. git commit -am "correct message"
```

## Exercise Timeline

| Action | Branch | Status |
|--------|--------|--------|
| Start feature | feature/payment-system | Active |
| Make commits 1-2 | feature/payment-system | Committed |
| Add unfinished files | feature/payment-system | Staged |
| Stash work | feature/payment-system | Saved |
| Create bugfix | bugfix/urgent-database-error | New branch |
| Fix and commit | bugfix/urgent-database-error | Complete |
| Return | feature/payment-system | Switched |
| Apply stash | feature/payment-system | Restored |
| Continue work | feature/payment-system | Resumed ✅ |

## Key Learnings

1. **Stash is Temporary** - Use for short-term work interruptions
2. **Preserve Context** - Helps you context-switch without losing work
3. **Workflow Efficiency** - Switch between tasks smoothly
4. **Clean Directory** - Allows safe branch switching
5. **Message Matters** - Good stash messages help identify content later

## Real-World Scenario

```
9:00 AM  - Start work on feature/payment-system
9:30 AM  - Make good progress, commit 2 times
9:45 AM  - Working on API endpoints (not committed yet)
9:55 AM  - Slack: "URGENT: Production down - database connections exhausted!"
10:00 AM - git stash (save unfinished work)
10:01 AM - git checkout bugfix branch (switch context)
10:05 AM - Fix database pool leak (2 commits)
10:10 AM - git checkout feature/payment-system (return)
10:11 AM - git stash pop (resume payment feature)
10:15 AM - Continue payment API development
10:30 AM - Commit payment feature
```

This workflow kept you productive, maintained code quality, and allowed rapid incident response.

## Completion Checklist

✅ Started feature branch with unfinished work
✅ Made initial commits to feature
✅ Created staged but uncommitted changes
✅ Stashed WIP with descriptive message
✅ Switched to urgent bugfix branch
✅ Completed and committed bugfix
✅ Returned to original feature branch
✅ Applied stash to resume work
✅ Continued feature development
✅ Documented the entire workflow

---
