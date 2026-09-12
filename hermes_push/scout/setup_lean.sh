#!/usr/bin/env bash
# One-time: create the persistent Lean project the scout compiles against. Takes a while the first time (it downloads Mathlib's cache).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PROJ="${SCOUT_LEAN_PROJECT:-$HERE/lean_project}"
if [ -d "$PROJ" ]; then echo "already present at $PROJ"; exit 0; fi
command -v lake >/dev/null || { echo "lake not found -- install Lean 4 via elan first: https://leanprover-community.github.io/get_started.html"; exit 1; }
cd "$HERE"
lake +leanprover-community/mathlib4:lean-toolchain new "$(basename "$PROJ")" math
cd "$PROJ"
lake exe cache get
printf 'import Mathlib\n' > Candidate.lean
lake env lean Candidate.lean && echo "SETUP OK: $PROJ is ready; the scout can now verify candidates."
