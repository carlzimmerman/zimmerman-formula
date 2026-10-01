#!/usr/bin/env bash
# CFG243_run_all.sh -- the frozen order, the stop rule, then the post-hoc extras (labelled), then every MUTATE / ROBUST check with the frozen expected exit code.
# Re-run: from this directory, `ZF_REPO=<repo root> bash CFG243_run_all.sh` (inside the repository the root is found by walking up, so `bash CFG243_run_all.sh` suffices).
# About 12 minutes.  Needs python3 with numpy, scipy, sympy and classy (CLASS); nothing is downloaded or installed; nothing outside this directory is written.
cd "$(dirname "$0")" || exit 1
export PYTHONDONTWRITEBYTECODE=1
unexpected=0
run() {   # run <expected exit> <label> <env assignment or -> <script>
  exp=$1; lab=$2; envv=$3; scr=$4
  if [ "$envv" = "-" ]; then python3 "$scr" > /dev/null 2>&1; rc=$?; else env "$envv" python3 "$scr" > /dev/null 2>&1; rc=$?; fi
  note=""; [ "$rc" != "$exp" ] && { note="  <-- UNEXPECTED"; unexpected=$((unexpected+1)); }
  echo "  $lab: expected exit $exp, observed $rc$note"
}
echo "== 1. controls (frozen K1-K5 plus the K6/K7 tool controls); a failed control stops the lane =="
python3 CFG243_controls.py > /dev/null 2>&1; rc=$?; echo "  CFG243_controls.py: exit $rc"
[ "$rc" != "0" ] && { echo "control failed: STOP"; exit 1; }
echo "== 2. GATE 1 COSMIC (frozen order: first) =="
python3 CFG243_cosmic.py > /dev/null 2>&1; echo "  CFG243_cosmic.py: exit $?"
echo "== 3. the frozen stop rule applies: COSMIC is a binding FAIL; the later gates run only as POST-HOC extras (labelled; never part of the verdict) =="
for s in CFG243_g0_legality_posthoc.py CFG243_amount_posthoc.py CFG243_hierarchy_posthoc.py CFG243_g3g4_ledger_posthoc.py; do
  python3 $s > /dev/null 2>&1; echo "  $s: exit $?"
done
echo "== 4. MUTATE controls (expected exit 1 = the control bites) and robustness checks (expected exit 0 = does NOT bite, as frozen) =="
run 1 "M1 z-independent creation (COSMIC)        " MUTATE=1 CFG243_cosmic.py
run 1 "M2 evaluation epoch z = 0 (COSMIC)        " MUTATE=2 CFG243_cosmic.py
run 1 "M3 non-local source (AMOUNT, post hoc)    " MUTATE=3 CFG243_amount_posthoc.py
run 1 "M4 host-aware source (HIERARCHY, post hoc)" MUTATE=4 CFG243_hierarchy_posthoc.py
run 1 "M5 counting rule imposed (G0-b, post hoc) " MUTATE=5 CFG243_g0_legality_posthoc.py
run 1 "M6 larger vacuum volume (G3/G4, post hoc) " MUTATE=6 CFG243_g3g4_ledger_posthoc.py
run 0 "R1 requirement 0.01 (expected NOT to bite)" ROBUST=1 CFG243_cosmic.py
run 0 "R2 delta_ta(1100) = 0.5 (expected NOT to bite)" ROBUST=2 CFG243_cosmic.py
echo "== 5. the verdict (the frozen stop rule; post-hoc cells printed separately) =="
python3 CFG243_verdict.py
echo "unexpected outcomes: $unexpected"
