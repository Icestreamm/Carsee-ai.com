#!/bin/zsh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
UPLOAD="/tmp/carsee-pages-upload"
PROJECT_NAME="${1:-carsee-website}"

# Prefer real Node; fall back to Cursor's bundled node if needed.
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.nvm/versions/node/$(ls "$HOME/.nvm/versions/node" 2>/dev/null | tail -1)/bin:$PATH"
if ! command -v node >/dev/null 2>&1; then
  CURSOR_NODE="/Applications/Cursor.app/Contents/Resources/app/resources/helpers/node"
  if [[ -x "$CURSOR_NODE" ]]; then
    export PATH="$(dirname "$CURSOR_NODE"):$PATH"
  fi
fi

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js is not installed."
  echo "Install it from https://nodejs.org (LTS), close Terminal, reopen, then run this script again."
  exit 1
fi

echo "Using node: $(command -v node) ($(node -v))"

cd "$ROOT"
if [[ ! -x "$ROOT/node_modules/.bin/wrangler" ]]; then
  if command -v npm >/dev/null 2>&1; then
    npm install
  else
    echo "npm not found. Install Node.js LTS from https://nodejs.org (includes npm), then retry."
    exit 1
  fi
fi

rm -rf "$UPLOAD"
mkdir -p "$UPLOAD"
rsync -a \
  --exclude '.git/' \
  --exclude 'node_modules/' \
  --exclude 'my-video/' \
  --exclude 'tools/' \
  --exclude '.DS_Store' \
  "$ROOT/" "$UPLOAD/"

echo "Uploading $(find "$UPLOAD" -type f | wc -l | tr -d ' ') files to Cloudflare Pages project: $PROJECT_NAME"
"$ROOT/node_modules/.bin/wrangler" pages deploy "$UPLOAD" --project-name="$PROJECT_NAME"
echo "Done."
