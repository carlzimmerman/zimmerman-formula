#!/bin/bash
# CFG195 re-run. From this directory: ZF_REPO=<repo root> bash run_all.sh   (about 5 min; the compare script opens CFG176's files and is last)
# Expected exit codes: nec_lp 0, sympy_algebra 0, q3_q5_numbers 0, freeform 1 (A3 kept failure), desi_bound 1 (I-3 kept failure); every MUTATE exits 1; compare 0.
cd "$(dirname "$0")" || exit 2
: "${ZF_REPO:?set ZF_REPO to the repository root}"
export ZF_REPO PYTHONDONTWRITEBYTECODE=1
for s in nec_lp sympy_algebra q3_q5_numbers freeform desi_bound; do python3 CFG195_$s.py > /dev/null 2>&1; echo "main $s rc=$?"; done
for pair in nec_lp:1 nec_lp:4 nec_lp:6 sympy_algebra:1 sympy_algebra:5 desi_bound:2 desi_bound:3 desi_bound:7; do s=${pair%%:*}; m=${pair##*:}; MUTATE=$m python3 CFG195_$s.py > /dev/null 2>&1; echo "MUTATE $s $m rc=$?"; done
python3 CFG195_compare.py > /dev/null 2>&1; echo "compare rc=$? (opens CFG176's files)"
