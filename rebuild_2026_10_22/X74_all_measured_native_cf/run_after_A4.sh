#!/bin/bash
# Run once X48 A4 has finished and X72's run_after_A4.sh has written x48_analyze_results_ng64_A4.json.
# Order fixed by FROZEN_CRITERIA.md (c3e69578c5): PRIMARY at both graded f*, then s16/s84 robustness, then MUTATE.
cd "$(dirname "$0")"
T=../X48_native_cf_zoom/x48_analyze_results_ng64_A4.json
[ -f $T ] || { echo "UNDECIDED: no A4 table"; exit 1; }
R() { PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x74_native_cf.py; echo "exit $? : $*"; }
for fs in 0.034 0.0615; do
  for sl in 2.7774425603108597 2.6756 3.0711; do X74_CF=$T X73_FSTAR=$fs X73_SLOPE=$sl R fs=$fs slope=$sl; done
done
X74_CF=$T X74_CFMULT=2 X73_FSTAR=0.034 R MUTATE
