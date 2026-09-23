#!/usr/bin/env bash
# One-time set-up per Claude Code session: what the build checks need.
set -e
python3 -m pip install --quiet --upgrade playwright pillow
python3 -m playwright install --with-deps chromium || python3 -m playwright install chromium
if ! command -v pdftoppm >/dev/null 2>&1; then
  (sudo apt-get update -qq && sudo apt-get install -y -qq poppler-utils) || (apt-get update -qq && apt-get install -y -qq poppler-utils) || echo "WARNING: poppler-utils (pdftoppm) not installed"
fi
(cd "$(dirname "$0")/build_kit" && npm install --no-save --silent docx >/dev/null 2>&1) || echo "WARNING: npm package docx not installed (needed only for the Εργασία 2 brief)"
echo "setup done"
