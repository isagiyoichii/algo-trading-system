#!/bin/bash

# === CONFIGURATION ===
COMMIT_MSG=${1:-"Auto-commit on $(date '+%Y-%m-%d %H:%M:%S')"}

# === EXECUTION ===
git add .
git commit -m "$COMMIT_MSG"
git push origin main
