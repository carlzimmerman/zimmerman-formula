#!/bin/bash
# grind.sh — launch the resumable depth-escalation grinder (see GRIND_README.md).
# caffeinate -i keeps the M4 Max awake for the multi-hour depths; output is appended to
# results_grind/grind.log. Extra args pass through to grind.py (e.g. ./grind.sh --force-depth 9).
set -euo pipefail
DIR="/Users/carlzimmerman/new_physics/project_atomos"
mkdir -p "$DIR/results_grind"
exec caffeinate -i python3 "$DIR/grind.py" --run "$@" 2>&1 | tee -a "$DIR/results_grind/grind.log"
