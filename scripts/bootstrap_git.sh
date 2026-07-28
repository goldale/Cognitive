#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
if [ -d .git ]; then
  echo "Git repository already exists." >&2
  exit 1
fi
git init
git add .
git commit -m "Bootstrap long-lived cognitive systems research state"
