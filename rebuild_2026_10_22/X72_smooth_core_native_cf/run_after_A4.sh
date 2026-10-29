#!/bin/bash
# Run once X48 A4 has finished (all 18 ng64 seeds at 1e13/1e14 written). Order fixed by FROZEN_CRITERIA.md (ba337e221c).
set -e
cd "$(dirname "$0")"
X48=../X48_native_cf_zoom
( cd $X48 && PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x48_analyze.py --ng 64 --tag A4 )
T=$X48/x48_analyze_results_ng64_A4.json
python3 score_prereg_cf_slope.py $T | tee prereg_cf_slope_score.out
for fs in 0.034 0.0615 0.20; do
  X72_CF=$T X71_FSTAR=$fs PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x72_native_cf.py || true
done
X72_CF=$T X72_CFMULT=2 X71_FSTAR=0.034 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x72_native_cf.py || true
grep -h -E "c_f table|VERDICT|G-OUT-M3 Z" x72_A4*.out
