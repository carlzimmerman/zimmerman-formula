#!/usr/bin/env bash
# Compile one candidate theorem file and report honestly. Usage: ./verify_lean.sh lean_candidates/cand_7.lean
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PROJ="${SCOUT_LEAN_PROJECT:-$HERE/lean_project}"
F="$1"
[ -f "$F" ] || { echo "VERIFY: no such file $F"; exit 2; }
[ -d "$PROJ" ] || { echo "VERIFY: no Lean project at $PROJ -- run ./setup_lean.sh first"; exit 2; }
if grep -q "sorry" "$F"; then echo "VERIFY: FAIL -- the file contains 'sorry', which is not a proof"; exit 1; fi
cp "$F" "$PROJ/Candidate.lean"
NAMES=$(grep -oE '^[[:space:]]*theorem[[:space:]]+[A-Za-z_][A-Za-z0-9_'"'"']*' "$F" | awk '{print $2}')
[ -n "$NAMES" ] || { echo "VERIFY: FAIL -- no theorem declaration found"; exit 1; }
cd "$PROJ" || exit 2
OUT=$(lake env lean Candidate.lean 2>&1)
if echo "$OUT" | grep -q "error"; then
  echo "VERIFY: FAIL -- it does not compile. First errors:"; echo "$OUT" | grep -A2 error | head -12; exit 1
fi
{ echo "import Candidate"; for n in $NAMES; do echo "#print axioms $n"; done; } > Axioms.lean
AX=$(lake env lean Axioms.lean 2>&1)
echo "VERIFY: COMPILES, no sorry."
echo "$AX" | grep "depends on axioms" || echo "  (no axiom line returned -- check the theorem names)"
if echo "$AX" | grep "depends on axioms" | grep -vq "propext, Classical.choice, Quot.sound"; then
  echo "VERIFY: WARNING -- a theorem depends on axioms beyond the three standard ones. Report this, do not hide it."
fi
