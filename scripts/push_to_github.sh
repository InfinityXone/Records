#!/bin/bash
# Push the Genesis deployment package to the InfinityXone/Genesis-AI-Neural-Link repository.
#
# This script initialises a Git repository in the current directory (if
# none exists), sets the remote to the official GitHub repository,
# commits all files and force-pushes the changes.  Use with caution:
# this will overwrite the remote repository contents.

set -euo pipefail

REPO="git@github.com:InfinityXone/Genesis-AI-Neural-Link.git"
BRANCH="main"

cd "$(dirname "$0")/.."

if [ ! -d .git ]; then
  git init
fi
git branch -M "$BRANCH" || true
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO"
git add .
git commit -m "🚀 Deploy: PWA, unified scraper, resource allocator, knowledge scanner, new endpoints and CronJobs; commit fingerprint SHA256:CU5fTSz0sGTy1m3Yu2WLnbhe7lZ39mcSLf5xBf8DO/4" || true
git push -u origin "$BRANCH" --force

echo "✅ Pushed Genesis deployment to $REPO on branch $BRANCH."