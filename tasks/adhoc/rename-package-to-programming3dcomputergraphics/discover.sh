#!/bin/bash
# List every tracked line that mentions the old package name, for the worklog
# in data/. Run from anywhere; writes data/before.txt beside this script.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
cd "$(git -C "$here" rev-parse --show-toplevel)"
git grep -I -n -i intro3dgraphics >"$here/data/before.txt" || true
wc -l <"$here/data/before.txt"
