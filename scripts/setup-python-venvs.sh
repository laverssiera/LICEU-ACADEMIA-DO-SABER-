#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
APPS=(
  "apps/api-python"
  "apps/simulation-engine"
  "apps/ai-learning-engine"
)

for app in "${APPS[@]}"; do
  APP_DIR="$ROOT_DIR/$app"
  VENV_DIR="$APP_DIR/.venv"

  if [[ ! -d "$VENV_DIR" ]]; then
    python -m venv "$VENV_DIR"
  fi

  "$VENV_DIR/bin/python" -m pip install --upgrade pip >/dev/null
  "$VENV_DIR/bin/pip" install -r "$APP_DIR/requirements.txt" >/dev/null
  echo "venv ready: $app"
done
