#!/bin/bash
# X48 direct launch 2: the three 1e12 seeds + the ng 48 resolution check (single thread each, nice 15)
cd "$(dirname "$0")/../.."
L=rebuild_2026_10_22/X48_native_cf_zoom; pids=()
for spec in "1e12 1 38" "1e12 2 38" "1e12 3 38" "1e14 1 48"; do
  set -- $spec; W=$L/runs/M$1_s$2_ng$3; mkdir -p $W
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 15 python3 $L/x48_zoom.py --mass $1 --seed $2 --ng $3 --work $W --resume > $W/run.log 2>&1 &
  pids+=($!)
done
trap 'kill -TERM "${pids[@]}" 2>/dev/null; wait; exit 75' TERM INT
wait; echo "batch 2 finished"
