#!/usr/bin/env bash
# One-time set-up per Claude Code session: what the build checks need.
set -e
# Cloud sessions ship a Chromium for the global npm playwright: pin the Python package to that version so no other browser is downloaded.
PW=playwright
V=$(npm ls -g playwright --depth=0 2>/dev/null | grep -o 'playwright@[0-9]*\.[0-9]*' | head -1 | cut -d@ -f2)
[ -n "$V" ] && PW="playwright~=$V.0"
python3 -m pip install --quiet --upgrade "$PW" pillow pandas
python3 -m playwright install --with-deps chromium || python3 -m playwright install chromium
if ! command -v pdftoppm >/dev/null 2>&1; then
  (sudo apt-get update -qq && sudo apt-get install -y -qq poppler-utils) || (apt-get update -qq && apt-get install -y -qq poppler-utils) || echo "WARNING: poppler-utils (pdftoppm) not installed"
fi
(cd "$(dirname "$0")/build_kit" && npm install --no-save --silent docx >/dev/null 2>&1) || echo "WARNING: npm package docx not installed (needed only for the Εργασία 2 brief)"
# The decks load Commissioner from Google Fonts, which headless Chromium may not reach: install it locally, or every check runs on a fallback font.
if ! fc-list 2>/dev/null | grep -qi commissioner; then
  D=/usr/local/share/fonts/commissioner; mkdir -p "$D" 2>/dev/null || { D="$HOME/.fonts/commissioner"; mkdir -p "$D"; }
  curl -sS "https://fonts.googleapis.com/css2?family=Commissioner:wght@100..900" \
    | awk '/font-weight/{w=$2+0} /src: url/{match($0,/https:[^)]*/); print w, substr($0,RSTART,RLENGTH)}' \
    | while read -r w u; do curl -sSf -o "$D/Commissioner-$w.ttf" "$u" || true; done || true
  fc-cache -f >/dev/null 2>&1 || true
  fc-list 2>/dev/null | grep -qi commissioner || echo "WARNING: font Commissioner not installed (checks would run on a fallback font)"
fi
echo "setup done"
