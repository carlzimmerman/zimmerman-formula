#!/bin/bash
# CFG235 phase 2, in the FROZEN order.  Usage: ZF_REPO=<repo> bash CFG235_run_all.sh   (run from the directory holding the scripts)
# Nothing is written into the repo; outputs go next to the scripts.  About 12 minutes in total.
set -u
export PYTHONDONTWRITEBYTECODE=1
: "${ZF_REPO:?set ZF_REPO to the repository root}"
python3 CFG235_00_sample.py   > CFG235_00_sample.out   2>&1; echo "00_sample exit $?"            # must print the sample table first; exit 2 = mismatch
python3 CFG235_01_controls.py > CFG235_01_controls.out 2>&1; c=$?; echo "01_controls exit $c"    # exit 1 = a control failed (kept, reported)
if [ $c -ne 0 ]; then export CFG235_GATE_OVERRIDE=1; echo "controls failed: gate passed with an override banner (see README)"; fi
python3 CFG235_02_main.py     > CFG235_02_main.out     2>&1; echo "02_main exit $?"
for k in 1 2 3 4 5 6 7 8; do MUTATE=$k python3 CFG235_MUTATE.py > CFG235_MUTATE_$k.out 2>&1; echo "MUTATE $k exit $? (1 = the control bites)"; done
python3 CFG235_03_report.py   > CFG235_03_report.out   2>&1; echo "03_report exit $?"
