#!/bin/bash
export PYTHONHASHSEED=0 OMP_NUM_THREADS=1
for s in 303 1 2 3 4 5 6 7; do GH5_MUTATE=1 GH5_SEED=$s nice -n 15 python3 gh5_tsz_desi.py > /dev/null 2>&1; echo "seed $s exit $?"; done; echo NULLDONE
