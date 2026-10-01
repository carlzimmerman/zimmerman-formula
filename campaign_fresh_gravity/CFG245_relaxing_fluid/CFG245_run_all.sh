#!/bin/bash
# CFG245 phase 2: run exactly as frozen.  G0, T, then C, A, E (post-hoc extras if T binds), the 16 MUTATE controls with the frozen expected exit
# code beside the observed one, then the verdict.  Usage:  ZF_REPO=<repo root> bash CFG245_run_all.sh   (inside the repository the root is found by walking up)
# Python 3 with numpy, scipy, sympy; nothing is downloaded; the repository is only READ; every output is written next to this script.
cd "$(dirname "$0")" || exit 2
for f in CFG245_*.out CFG245_*_results.json; do [ -e "$f" ] && rm -f "$f"; done
exec > >(tee CFG245_run_all.out) 2>&1
unexpected=0
run_main () { echo "=== $1"; python3 "$1" > /dev/null 2>"$1.err"; rc=$?; if [ $rc -ne 0 ]; then echo "  main run exit $rc (expected 0)"; unexpected=$((unexpected+1)); fi; rm -f "$1.err"; }
run_main CFG245_G0_target.py
run_main CFG245_T_timescale.py
run_main CFG245_C_clusters.py
run_main CFG245_A_supply.py
run_main CFG245_E_ledger.py
run_mut () { # script id expected_exit
  MUTATE=$2 python3 "$1" > /dev/null 2>&1; rc=$?
  flag=""; if [ "$rc" != "$3" ]; then flag="  <-- UNEXPECTED"; unexpected=$((unexpected+1)); fi
  echo "MUTATE $2 ($1): expected exit $3, observed $rc$flag"
}
run_mut CFG245_G0_target.py MG1 1
run_mut CFG245_G0_target.py MG2 1
run_mut CFG245_G0_target.py MG3 1
run_mut CFG245_T_timescale.py MT1 1
run_mut CFG245_T_timescale.py MT2a 1
run_mut CFG245_C_clusters.py MT2b 1
run_mut CFG245_E_ledger.py MT3 1
run_mut CFG245_A_supply.py MM1 1
run_mut CFG245_C_clusters.py MC1 1
run_mut CFG245_C_clusters.py MC2 1
run_mut CFG245_A_supply.py MA1 1
run_mut CFG245_A_supply.py MA2 1
run_mut CFG245_E_ledger.py ME1 1
run_mut CFG245_E_ledger.py ME2 1
run_mut CFG245_T_timescale.py MN1 0
run_mut CFG245_T_timescale.py MN2 0
python3 CFG245_verdict.py
echo "unexpected outcomes: $unexpected"
