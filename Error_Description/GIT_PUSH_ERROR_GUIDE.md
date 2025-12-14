# Git Push Non-Fast-Forward Error Guide

## Error Description

The error you encountered was:
```
! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/...'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart.
```

This occurs when your local repository branch is **behind the remote repository**, meaning someone else (or another instance) pushed changes to the remote that your local version doesn't have.

---

## How to Identify This Error

When you run `git push`, look for these keywords:

| Keyword | Meaning |
|---------|---------|
| `[rejected]` | Push was rejected |
| `non-fast-forward` | Your local history doesn't include all remote commits |
| `behind its remote counterpart` | Your branch is outdated |
| `Updates were rejected` | Generic rejection message |

---

## Step-by-Step Solution

### **Step 1: Attempt Initial Pull**

Fetch remote changes and merge them locally:

```bash
git pull origin main
```

**Expected Output:**
```
From https://github.com/username/repo
 * branch            main       -> FETCH_HEAD
Auto-merging ...
```

---

### **Step 2: If You Get "Divergent Branches" Error**

If the pull fails with: `Need to specify how to reconcile divergent branches`

Configure git to use merge strategy:

```bash
git config pull.rebase false
```

Then try pulling again:

```bash
git pull origin main
```

---

### **Step 3: If You Get "Unrelated Histories" Error**

If the pull fails with: `fatal: refusing to merge unrelated histories`

Allow merging branches with different histories:

```bash
git pull --allow-unrelated-histories origin main
```

---

### **Step 4: If Merge Conflict Occurs**

The merge will fail if there are conflicting changes. You'll see conflict markers in files:

```
<<<<<<< HEAD
your local changes
=======
remote changes
>>>>>>> branch-name
```

**Option A - Keep Your Local Changes (Force Push):**

```bash
git merge --abort
git push -f origin main
```

The `-f` (force) flag overwrites remote with your local version.

**Option B - Keep Remote Changes:**

```bash
git merge --abort
git reset --hard origin/main
git push origin main
```

---

### **Step 5: Verify Success**

Attempt the push again:

```bash
git push origin main
```

**Successful Output:**
```
To https://github.com/username/repo.git
   2e6ad80...d932c82 main -> main (forced update)
```

---

## Quick Reference Flowchart

```
git push fails (non-fast-forward)
    ↓
├─→ git pull origin main
    │
    ├─ ✓ Success → git push origin main
    │
    ├─ ✗ Divergent branches error
    │   ↓
    │   git config pull.rebase false
    │   git pull origin main
    │
    ├─ ✗ Unrelated histories error
    │   ↓
    │   git pull --allow-unrelated-histories origin main
    │
    └─ ✗ Merge conflict
        ↓
        Option A (Keep local):
        git merge --abort && git push -f origin main ✓
        
        Option B (Keep remote):
        git merge --abort && git reset --hard origin/main
```

---

## Real-World Example: Commands Used

Here are the exact commands executed to resolve your error:

```bash
# Step 1: Initial push attempt (FAILED)
git push -u origin main

# Step 2: Pull remote changes
git pull origin main

# Step 3: Configure merge strategy
git config pull.rebase false

# Step 4: Attempt pull with unrelated histories
git pull --allow-unrelated-histories origin main
# Result: Merge conflict in .gitignore

# Step 5: Abort merge and force push local version
git merge --abort
git push -f origin main
# Result: SUCCESS ✓
```

---

## When to Use Each Option

| Scenario | Command | Use Case |
|----------|---------|----------|
| Standard sync needed | `git pull origin main` | Your code doesn't conflict with remote |
| Merge conflicts exist | `git merge --abort` | Need to decide which version to keep |
| Keep your changes | `git push -f origin main` | Your local version is the correct one |
| Keep remote changes | `git reset --hard origin/main` | Remote version is correct, discard local |
| Different branch histories | `git pull --allow-unrelated-histories` | Merging two projects with separate Git histories |

---

## Key Takeaways

✅ **Always pull before pushing** - This is the golden rule of Git collaboration

✅ **Merge conflicts are normal** - They occur when both local and remote have changes in the same files

✅ **Use `-f` (force) carefully** - It overwrites remote history; only use when you're certain

✅ **Understand your strategy** - Know whether to keep local or remote changes before committing to a solution

---

## Prevention Tips

1. **Pull frequently** - Run `git pull` before starting work
2. **Communicate with team** - Let others know what you're working on
3. **Use feature branches** - Keep main branch stable, work on separate branches
4. **Review before push** - Always check your changes before pushing

```bash
# Before starting work
git pull origin main

# After making changes, before pushing
git status
git diff
git push origin main
```

---

## Common Git Commands Reference

```bash
# View git history
git log --oneline

# Check current branch and status
git status

# View differences between local and remote
git diff origin/main

# View all branches
git branch -a

# Stash changes temporarily
git stash

# Apply stashed changes
git stash pop

# Reset to previous commit (keep changes)
git reset HEAD~1

# Reset to previous commit (discard changes)
git reset --hard HEAD~1
```

---

*Last Updated: December 11, 2025*
