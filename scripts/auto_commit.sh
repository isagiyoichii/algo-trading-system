#!/bin/bash

# === CONFIGURATION ===
PROJECT_ROOT="/c/Users/ronit/OneDrive/Documents/Algo_Trader/algo-trading-system"
LOG_FILE="$PROJECT_ROOT/logs/auto_commit.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
COMMIT_MSG=${1:-"Auto-commit on $TIMESTAMP"}

# === LOGGING EXECUTION ===
echo "[$TIMESTAMP] Starting auto commit..." >> "$LOG_FILE"

cd "$PROJECT_ROOT"

git add . >> "$LOG_FILE" 2>&1

if git diff --cached --quiet; then
  echo "[$TIMESTAMP] No changes to commit." >> "$LOG_FILE"
  exit 0
fi

git commit -m "$COMMIT_MSG" >> "$LOG_FILE" 2>&1
git push origin main >> "$LOG_FILE" 2>&1

echo "[$TIMESTAMP] Commit complete: $COMMIT_MSG" >> "$LOG_FILE"
