#!/bin/bash
# CFG168 full re-run. Usage: ZF_REPO=<repo> bash run_all.sh   (from this directory). Prints rc per step.
set -u
export PYTHONDONTWRITEBYTECODE=1
: "${ZF_REPO:?set ZF_REPO}"
python3 cfg168_main.py > CFG168_main.out 2> CFG168_main.err; echo "main rc=$? (expect 0)"
for k in 1 2 3 4 5 6 7; do CFG168_MUTATE=$k python3 cfg168_main.py > CFG168_MUTATE_$k.out 2> CFG168_MUTATE_$k.err; echo "MUTATE $k rc=$? (1 = bites; 5 and 7 informational)"; done
python3 cfg168_attacks.py > CFG168_attacks.out 2> CFG168_attacks.err; echo "attacks rc=$?"
python3 cfg168_null.py > CFG168_null.out 2> CFG168_null.err; echo "null rc=$?"
CFG168_NULL_OFFSET=0 python3 cfg168_null.py > CFG168_null_v0_nooffset.out 2> CFG168_null_v0_nooffset.err; echo "null v0 (no pipeline offset in mocks) rc=$?"
python3 cfg168_diag_postcomparison.py > CFG168_diag_postcomparison.out 2>&1; echo "diag (post-comparison) rc=$?"
for f in CFG168_*.err; do sed -i.bak -e "s#${ZF_REPO}#<repo>#g" -e "s#$(pwd)#<scratch>#g" "$f"; rm -f "$f.bak"; done
