#!/bin/bash
# RUN_ALL.sh -- the kappa-forced re-run, as a plain sequential job (no workflow harness).
# Gate B binding is the make-or-break: if kappa-free expressions can still pass, the whole
# re-run is meaningless, so that check runs FIRST and aborts everything on failure.
# Then the published-config regression must reproduce committed counts EXACTLY.
# Only then do the depth sweeps run.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1
OUT=results_kappa_rerun
mkdir -p "$OUT"
log() { echo "[$(date -u +%H:%M:%SZ)] $*"; }

log "STEP 1/4  prove Gate B binds under forced={3,kappa}  (ABORTS ALL if it does not)"
python3 -u prove_gate_b_binds.py > "$OUT/01_gate_b_binds.txt" 2>&1
rc=$?
tail -20 "$OUT/01_gate_b_binds.txt"
if [ $rc -ne 0 ]; then
  log "GATE B DOES NOT BIND (exit $rc) -- ABORTING. The re-run would be meaningless."
  exit 1
fi
log "STEP 1 ok"

log "STEP 2/4  regression: published forced set must reproduce committed counts EXACTLY"
python3 -u regression_published.py > "$OUT/02_regression.txt" 2>&1
rc=$?
tail -20 "$OUT/02_regression.txt"
if [ $rc -ne 0 ]; then
  log "REGRESSION FAILED (exit $rc) -- ABORTING. Cannot trust a new path that breaks the old one."
  exit 1
fi
log "STEP 2 ok"

log "STEP 3/4  value-set delta (published vs kappa) for the record"
python3 -u value_set_delta.py > "$OUT/03_value_delta.txt" 2>&1 || true
tail -12 "$OUT/03_value_delta.txt"

log "STEP 4/4  depth sweeps with forced={3,kappa}"
for D in 5 6 7 8; do
  log "  depth $D ..."
  python3 -u run_forced_pair_depth.py --depth "$D" --mode kappa \
      > "$OUT/04_depth${D}_kappa.txt" 2>&1
  rc=$?
  grep -iE "distinct|raw|hits|CERT|certified|gate_status" "$OUT/04_depth${D}_kappa.txt" | tail -8
  log "  depth $D exit $rc"
  [ $rc -ne 0 ] && log "  depth $D FAILED -- continuing to next depth, see log"
done

log "DONE. outputs in $(pwd)/$OUT"
grep -ihE "certified|CERT=" "$OUT"/04_depth*_kappa.txt 2>/dev/null | tail -12
