# Exercise 3: Reset vs Revert — Undo Mistakes Safely

## Scenario Recap
A bad deployment was pushed to production. We demonstrated using `git revert` to safely undo the mistake. Now we explore the differences between `git revert` and `git reset`.

## Part 1: What We Already Did (git revert)

```bash
# Commit: 8a13cf7 "Update app mode - BROKEN CONFIG"
# This broke the production configuration
# Solution: git revert -m 1 8a13cf7
# Result: Commit 9234992 "Revert 'Update app mode - BROKEN CONFIG'"
```

**Why revert is safe:**
- Creates a NEW commit that undoes changes
- Preserves commit history (you can see what went wrong)
- Safe for shared/published branches
- Other developers won't have conflicts

---

## Part 2: Alternative - git reset --soft

**What it does:**
- Moves HEAD back to a previous commit
- Keeps changes in the staging area
- History is rewritten (dangerous for shared branches)
- Allows you to re-commit with better organization

**When to use:**
- Before pushing (local branches only)
- You want to reorganize commits
- Working alone on a feature branch

**Example workflow:**
```bash
# Suppose we have commits A -> B -> C (broken) -> D
# We want to undo C but keep its changes

# Step 1: Reset to before the broken commit
git reset --soft C^  # or: git reset --soft C~1

# Step 2: Changes from C are now staged
git status  # Shows: Changes to be committed

# Step 3: Either:
# - Modify the changes and commit differently
# - Or just re-commit with a better message
git commit -m "Fixed configuration properly"
```

**Advantages:**
- Can reorganize commits before committing
- Useful for squashing commits
- Interactive control over what gets committed

**Disadvantages:**
- Rewrites history (only for local branches!)
- Doesn't work well for shared branches
- Can confuse team members if used carelessly

---

## Part 3: Alternative - git reset --hard

**What it does:**
- Moves HEAD back to previous commit
- DISCARDS all changes (working directory reset)
- History is completely rewritten
- Point of no return (unless using git reflog)

**When to use:**
- You want to completely discard changes
- Emergency recovery (not recommended for shared branches)
- Last resort when things are completely broken

**Example workflow:**
```bash
# Suppose we have commits A -> B -> C (broken) -> D -> E
# We want to completely undo the last 2 commits and lose all their changes

# Step 1: Reset hard to 2 commits ago
git reset --hard HEAD~2

# Step 2: Your working directory is now at commit C
# Everything from D and E is GONE (unless in reflog)
```

**Advantages:**
- Complete cleanup of unwanted changes
- Gets you back to a known good state
- Fast for emergency rollbacks

**Disadvantages:**
- DESTROYS changes (they're gone unless in git reflog)
- Rewrites history (breaks shared branches)
- Dangerous to use carelessly

---

## Part 4: When to Use Each Strategy

### Use `git revert` when:
✅ Changes are already published/pushed
✅ Others might be using the branch
✅ You want to keep history visible (for audit/debugging)
✅ Working on main/develop/production branches
✅ You need a safe, reversible undo

### Use `git reset --soft` when:
✅ Changes are local (not pushed)
✅ You want to reorganize commits
✅ Squashing multiple commits into one
✅ Re-doing a commit with better message/changes
✅ You want to keep the changes but redo the commits

### Use `git reset --hard` when:
✅ Changes are local (not pushed)
✅ You want to completely discard everything
✅ Emergency: need to get back to known good state
✅ You're sure the changes are unwanted
⚠️ NEVER on shared branches

---

## Part 5: Practical Demonstration

### Demonstration 1: git revert (Already completed above)
**Commits: 8a13cf7 -> 9234992**
- Initial broken commit: 8a13cf7 "Update app mode - BROKEN CONFIG"
- Revert commit: 9234992 "Revert 'Update app mode - BROKEN CONFIG'"
- History shows both commits, history is preserved

### Demonstration 2: git reset --soft (Simulated)

If we had instead done:
```bash
git reset --soft 8a13cf7^   # Reset to before the broken commit
# Files would be in staging area
# We could then recommit with better organization
```

**Benefits over revert:**
- Cleaner history (no "Revert" commit)
- Can reorganize multiple changes at once
- Staging area gives you control over what goes in

**Drawbacks:**
- Doesn't work if already pushed
- History is rewritten (teammates see different log)
- Less transparent about what was wrong

### Demonstration 3: git reset --hard (Simulated)

If we had done:
```bash
git reset --hard 8a13cf7^   # Go back and lose everything
# Working directory matches 8a13cf7^
# Commits after this are gone from history
# Can only recover via git reflog
```

**Benefits:**
- Complete cleanup in one command
- Fast for emergency situations
- Working directory is guaranteed clean

**Drawbacks:**
- Changes are DESTROYED
- History is completely rewritten
- Recovery only through git reflog (limited time window)
- Very dangerous on shared branches

---

## Key Takeaways

| Strategy | History | Safety | Shared Branches | Use Case |
|----------|---------|--------|-----------------|----------|
| **git revert** | Preserved | ✅ Safe | ✅ Yes | Published changes |
| **git reset --soft** | Rewritten | ⚠️ Local only | ❌ No | Reorganizing commits |
| **git reset --hard** | Destroyed | ⚠️ Local only | ❌ No | Emergency cleanup |

---

## When Things Go Wrong

If you use `reset` and regret it:
```bash
# Recent changes might be in git reflog
git reflog                    # See your recent HEAD positions
git reset --hard <reflog-id>  # Recover to that state
```

But this is unreliable. **Prevention is better: only use reset on local branches!**

---

## Summary

**Why we demonstrated `git revert` instead of `reset`:**
- This change was "pushed to production" (shared branch scenario)
- Revert is the safe, professional choice
- Creates an auditable history showing what went wrong
- Other developers won't have merge conflicts

**Reset variations are useful for:**
- Local feature branches
- Cleaning up commits before pushing
- Reorganizing work-in-progress

**The golden rule:**
> "Once you push it, revert it. Before you push it, reset it."

