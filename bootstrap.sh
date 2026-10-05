#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UPSTREAM="$ROOT/_upstream"
WORKSPACE="$ROOT/workspace"
OVERLAY="$ROOT/overlay"

if [ ! -d "$UPSTREAM/.git" ] && [ ! -f "$UPSTREAM/.git" ]; then
  echo "Upstream submodule is not initialized."
  echo "Run: git submodule update --init --recursive"
  exit 1
fi

if [ ! -f "$UPSTREAM/AGENTS.md" ] || [ ! -d "$UPSTREAM/.claude" ]; then
  echo "_upstream does not look like ai-job-search."
  exit 1
fi

if [ -e "$WORKSPACE" ]; then
  stamp="$(date +%Y%m%d-%H%M%S)"
  backup="$ROOT/workspace-backup-$stamp"
  echo "Moving existing workspace to: $backup"
  mv "$WORKSPACE" "$backup"
fi

echo "Creating clean workspace from pinned upstream..."
mkdir -p "$WORKSPACE"

if command -v rsync >/dev/null 2>&1; then
  rsync -a --exclude='.git' "$UPSTREAM/" "$WORKSPACE/"
else
  cp -a "$UPSTREAM/." "$WORKSPACE/"
  rm -rf "$WORKSPACE/.git"
fi

echo "Applying India/new-grad overlay..."
python3 "$OVERLAY/install_overlay.py" "$WORKSPACE"

echo
echo "Workspace ready: $WORKSPACE"
echo "Next:"
echo "  cd workspace"
echo "  # fill exact resume details / run /setup"
echo "  # then run /daily-batch"
