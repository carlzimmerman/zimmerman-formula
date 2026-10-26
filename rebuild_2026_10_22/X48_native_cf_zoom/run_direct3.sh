#!/bin/bash
# X48 direct launch 3 (A1): the eight remaining ng 48 runs (single thread each, nice 15); --resume continues from any checkpoint
cd "$(dirname "$0")/../.."
L=rebuild_2026_10_22/X48_native_cf_zoom; pids=()
for spec in "1e14 2" "1e14 3" "1e13 1" "1e13 2" "1e13 3" "1e12 1" "1e12 2" "1e12 3"; do
  set -- $spec; W=$L/runs/M$1_s$2_ng48; mkdir -p $W
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 15 python3 $L/x48_zoom.py --mass $1 --seed $2 --ng 48 --work $W --resume >> $W/run.log 2>&1 &
  pids+=($!)
done
trap 'kill -TERM "${pids[@]}" 2>/dev/null; wait; exit 75' TERM INT
wait; echo "batch 3 finished"
