#!/usr/bin/env bash
# Build upload packages for Claude Cowork (plugin zip) and claude.ai (skill file).
# Designed and built by Legion Code Inc.
# Usage: tools/build-dist.sh   (run from anywhere; requires zip)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$ROOT/dist"
VERSION="$(node -e 'console.log(require(process.argv[1]).version)' "$ROOT/plugins/webapp-capture/.claude-plugin/plugin.json")"
EXCLUDES=(-x '*/node_modules/*' -x '*.DS_Store' -x '*/.capture/*')

command -v zip >/dev/null || { echo "zip is required" >&2; exit 1; }
rm -rf "$DIST" && mkdir -p "$DIST"

# Cowork and Claude Code: the whole plugin, folder at the archive root.
(cd "$ROOT/plugins" && zip -qr "$DIST/webapp-capture-plugin-$VERSION.zip" webapp-capture "${EXCLUDES[@]}")

# claude.ai (Settings > Capabilities > Skills): the skill alone, folder at the archive root.
(cd "$ROOT/plugins/webapp-capture/skills" && zip -qr "$DIST/webapp-capture-stinger-$VERSION.skill" webapp-capture-stinger "${EXCLUDES[@]}")

# Integrity: the skill frontmatter must use only the six portable fields.
FRONT="$(awk '/^---$/{n++; next} n==1' "$ROOT/plugins/webapp-capture/skills/webapp-capture-stinger/SKILL.md" | grep -E '^[a-z-]+:' | cut -d: -f1 | sort -u | tr '\n' ' ')"
for key in $FRONT; do
  case "$key" in name|description|license|compatibility|metadata|allowed-tools) ;; *) echo "non-portable frontmatter key: $key" >&2; exit 1 ;; esac
done

(cd "$DIST" && shasum -a 256 ./* > SHA256SUMS)
ls -la "$DIST"
cat "$DIST/SHA256SUMS"
