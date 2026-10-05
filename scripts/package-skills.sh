#!/usr/bin/env bash
# Zip every skill for Claude.ai upload: dist/<skill>.zip with the skill folder at the root.
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf dist && mkdir -p dist
for dir in plugins/seo-dashboard/skills/*/; do
  name="$(basename "$dir")"
  (cd plugins/seo-dashboard/skills && zip -qr "../../../dist/${name}.zip" "$name" -x '*.DS_Store')
  echo "dist/${name}.zip"
done
