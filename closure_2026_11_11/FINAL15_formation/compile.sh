#!/bin/sh
# FINAL-15 (FORMATION): compile the Lean certification files.
#
# This lane folder is NOT a lake project, so a bare `lean FINAL15.lean` cannot resolve Mathlib.
# The repository's Mathlib project lives at fable_independent_2026/lean_2026; `lake env lean` puts the
# built Mathlib on the search path. Nothing outside this folder is modified.
#
#   FINAL15.lean        must compile (exit 0)
#   FINAL15_MUTATE.lean must FAIL    (exit 1, one error per false statement)
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
LAKE=$(cd "$HERE/../../../fable_independent_2026/lean_2026" && pwd)
cd "$LAKE"
lake env lean "$HERE/FINAL15.lean"        > "$HERE/compile.txt"        2>&1 || { echo "exit=$?" >> "$HERE/compile.txt"; }
lake env lean "$HERE/FINAL15_MUTATE.lean" > "$HERE/compile_MUTATE.txt" 2>&1 || { echo "exit=$?" >> "$HERE/compile_MUTATE.txt"; }
echo "FINAL15.lean exit:        $(tail -1 "$HERE/compile.txt")"
echo "FINAL15_MUTATE.lean exit: $(tail -1 "$HERE/compile_MUTATE.txt")"
