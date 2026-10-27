#!/bin/bash
# runs the R-X10 2D reproductions for one footing, sequentially
cd "$(dirname "$0")/.."
export OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MallocMediumZone=0
for h in 20 10 5; do
  nice -n 15 python3 x12_2d.py --mass MW --foot $1 --h $h >> work/x2d_$1.log 2>&1
  echo "exit $? h $h" >> work/x2d_$1.log
done
