#!/bin/bash
# After A4's CE1 rerun writes its tables, rerun FC1's grade on them (same script, --A4). Outputs FC1_A4_*; commits nothing. kappa = 1/2 FITTED; not theory closed.
cd "$(dirname "$0")" || exit 1
CE=../CE1_converged_eta_grade
until [ -f "$CE/ce1_a4_results.json" ] && [ -f "$CE/CE1_A4_p84_fs0.0615_cf_table.json" ]; do sleep 300; done
sleep 60
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 fc1_grade.py --A4 > fc1_a4_run.log 2>&1
