#!/bin/bash
# AMENDMENT A2 h = 5 rung run directly (queue stalled since 10-31 behind L1_calib_512; owner approved 2026-11-04)
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
for foot in canonical alt; do
  nice -n 15 python3 khronon_fluid.py --mode sc --foot $foot --orbit O1 --ti 9 --h 5 --dt 0.005 --extend --resume >> h5_direct.log 2>&1
  echo "done $foot rc $?" >> h5_direct.log
done
