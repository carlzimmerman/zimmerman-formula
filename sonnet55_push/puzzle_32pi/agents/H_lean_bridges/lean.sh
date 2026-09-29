#!/usr/bin/env bash
# lean.sh: run the Lean 4.34.0-rc2 + Mathlib toolchain of the (read-only) library fable_independent_2026/lean_2026 on files of THIS directory.
# Usage: ./lean.sh [-o] File.lean     (-o also writes build/File.olean so later files can `import File`)
# Nothing is written into fable_independent_2026/lean_2026 (only `lake env` is queried, to obtain LEAN_PATH).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LEANLIB="$HERE/../../../../fable_independent_2026/lean_2026"
LP="$(cd "$LEANLIB" && lake env printenv LEAN_PATH)"
LEAN="$(cd "$LEANLIB" && lake env which lean)"
mkdir -p "$HERE/build"
cd "$HERE"
if [ "${1:-}" = "-o" ]; then
  shift; f="$1"; m="${f%.lean}"
  LEAN_PATH="$LP:$HERE/build" "$LEAN" -o "build/$m.olean" "$f"
else
  LEAN_PATH="$LP:$HERE/build" "$LEAN" "$1"
fi
