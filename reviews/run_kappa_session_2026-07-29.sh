#!/bin/bash
# run_kappa_session_2026-07-29.sh -- re-run every script from the 2026-07-29 kappa/spectral
# session and capture its full output, so the whole chain is self-verifying from a clean clone.
#
# Order is the order the results were derived, because later scripts depend on earlier ones:
#   1. circularity   -- closes the LOCAL route (all committed kernel conditions scale-invariant)
#   2. weight swing   -- opens the GLOBAL route (W_above = 1/(pi Z), exact bijection)
#   3. kms bootstrap  -- zero-parameter thermal condition; also downgrades the swing's 2pi claim
#   4. reduction      -- a0 = kappa c sqrt(G rho_L); W_above LINEAR in kappa   <-- key result
#   5. forced attempt -- 2 pre-registered principles, both miss
#   6. dissipative    -- RETRACTS "spectral side wants kappa=1" (my wrong premise)
#   7. thermal no-go  -- exhausts forced-constant saturation targets
#   8. three classes  -- exhausts the last three classes
#   9. germ provenance-- sqrt(8pi/3) is GR x FRW, not the framework's number
#  10. THRESHOLD      -- (project_atomos) settles interlock k_min
#  11. INTERLOCK      -- (project_atomos) permutation-calibrated search + planted controls
#  12. kappa equiv    -- (project_atomos) forcing kappa opens 336 unreachable values
#
# Usage:  bash reviews/run_kappa_session_2026-07-29.sh
set -u
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ATOMOS="$HOME/new_physics/project_atomos"
OUT="$REPO/reviews/outputs_kappa_session_2026-07-29"
mkdir -p "$OUT"

pass=0; fail=0; skip=0
run() {   # run <label> <workdir> <cmd...>
  local label="$1"; shift
  local wd="$1"; shift
  if [ ! -d "$wd" ]; then
    printf '  %-42s SKIP (no %s)\n' "$label" "$wd"; skip=$((skip+1)); return
  fi
  if [ ! -f "$wd/$1" ]; then
    printf '  %-42s SKIP (missing %s)\n' "$label" "$1"; skip=$((skip+1)); return
  fi
  ( cd "$wd" && python3 -u "$@" ) > "$OUT/$label.txt" 2>&1
  local rc=$?
  local n; n=$(wc -l < "$OUT/$label.txt" | tr -d ' ')
  if [ "$rc" -eq 0 ]; then
    printf '  %-42s exit 0   (%s lines)\n' "$label" "$n"; pass=$((pass+1))
  else
    printf '  %-42s exit %-3s (%s lines) <-- FAILED\n' "$label" "$rc" "$n"; fail=$((fail+1))
  fi
}

echo "=== 2026-07-29 kappa / spectral session -- full re-run ==="
echo "  repo   : $REPO"
echo "  atomos : $ATOMOS"
echo "  outputs: $OUT"
echo

echo "-- zimmerman-formula/reviews --"
run 01_bootstrap_circularity   "$REPO" reviews/mi_bootstrap_circularity_2026.py
run 02_spectral_weight_swing   "$REPO" reviews/mi_spectral_weight_swing_2026.py
run 03_kms_bootstrap           "$REPO" reviews/mi_spectral_kms_bootstrap_2026.py
run 04_kappa_reduction         "$REPO" reviews/mi_kappa_spectral_reduction_2026.py
run 05_forced_weight_attempt   "$REPO" reviews/mi_forced_weight_attempt_2026.py
run 06_dissipative_ident       "$REPO" reviews/mi_dissipative_identification_2026.py
run 07_thermal_class_nogo      "$REPO" reviews/mi_thermal_class_nogo_2026.py
run 08_three_classes           "$REPO" reviews/mi_three_classes_2026.py
run 09_atomos_germ_provenance  "$REPO" reviews/mi_atomos_germ_provenance_2026.py

echo
echo "-- project_atomos (local-only working copy) --"
run 10_THRESHOLD               "$ATOMOS" THRESHOLD.py
run 11_INTERLOCK_selftest      "$ATOMOS" INTERLOCK_SEARCH.py --selftest --nperm 200
run 12_kappa_forced_equiv      "$ATOMOS" audit_interlock/kappa_forced_equivalence.py

echo
echo "=== SUMMARY: $pass passed, $fail failed, $skip skipped ==="
echo "    outputs in $OUT"
[ "$fail" -eq 0 ] || echo "    NOTE: a nonzero exit means a self-check inside that script FAILED."
exit $([ "$fail" -eq 0 ] && echo 0 || echo 1)
