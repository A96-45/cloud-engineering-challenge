#!/bin/bash

# Git Exercises - Push to GitHub Script
# This script pushes all completed exercise branches to GitHub

set -e  # Exit on error

echo "=========================================="
echo "Git Exercises - Push to GitHub"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a Git repository"
    exit 1
fi

# Display current status
echo "📊 Current Repository Status:"
echo "============================="
git remote -v
echo ""
echo "Local branches:"
git branch -a | grep -v remotes || echo "No branches"
echo ""

# Get user confirmation
echo "⚠️  WARNING: This will push all local branches to GitHub"
echo "Repository: https://github.com/A96-45/cloud-engineering-challenge"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Push cancelled"
    exit 1
fi

echo ""
echo "🚀 Pushing to GitHub..."
echo "========================"

# Try to push with main branch first
echo ""
echo "Pushing main branch..."
git push origin main && echo "✅ main branch pushed" || echo "⚠️ main push had issues"

# Push develop
echo ""
echo "Pushing develop branch..."
git push origin develop && echo "✅ develop branch pushed" || echo "⚠️ develop push had issues"

# Push release branch
echo ""
echo "Pushing release/v1.2..."
git push origin release/v1.2 && echo "✅ release/v1.2 pushed" || echo "⚠️ release/v1.2 push had issues"

# Push exercise branches
echo ""
echo "Pushing exercise branches..."

branches=(
    "exercise/4-team-collaboration"
    "feature/api"
    "hotfix/login-failure"
    "bugfix/urgent-database-error"
    "feature/payment-system"
    "exercise/8-secret-recovery"
    "exercise/9-cicd-workflow"
    "exercise/10-gitops"
    "feature/k8s-scaling"
    "feature/k8s-ingress-enhancement"
    "feature/k8s-resource-limits"
)

for branch in "${branches[@]}"; do
    echo "  Pushing $branch..."
    git push origin "$branch" && echo "    ✅ Pushed" || echo "    ⚠️ Failed (may already exist)"
done

echo ""
echo "=========================================="
echo "✅ Push Complete!"
echo "=========================================="
echo ""
echo "Verify on GitHub:"
echo "🔗 https://github.com/A96-45/cloud-engineering-challenge"
echo ""
echo "Check branches:"
echo "  git branch -a"
echo "  git fetch origin"
echo ""
echo "View specific branches:"
git branch -a | grep -E "(exercise|feature|hotfix|bugfix|release)" | sed 's/^/  /'
echo ""
