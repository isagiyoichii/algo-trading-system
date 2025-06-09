#!/bin/bash

# === CONFIGURATION ===
COMMIT_MSG=${1:-"Auto-commit on $(date '+%Y-%m-%d %H:%M:%S')"}

# === EXECUTION ===
echo "[INFO] Staging all changes..."
git add .

if git diff --cached --quiet; then
  echo "[INFO] No changes to commit."
  exit 0
fi

echo "[INFO] Committing with message: $COMMIT_MSG"
git commit -m "$COMMIT_MSG"
echo "[INFO] Pushing to origin/main"
git push origin main
