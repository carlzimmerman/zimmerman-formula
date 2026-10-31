#!/bin/bash
# X80: 1e10 and 1e11 zooms (seeds 1-9 ng 64 + seeds 1-3 ng 48), all concurrently, single thread each, nice 15; X48's x48_zoom.py
# unchanged, with ZK1's compiled accel (AMENDMENT A2); --resume continues from any checkpoint; SIGTERM -> children checkpoint, exit 75
cd "$(dirname "$0")/../.."
L=rebuild_2026_10_22/X48_native_cf_zoom
run() { W=$L/runs/M$1_s$2_ng$3; mkdir -p $W; touch $W/ZK1_SWITCHED; OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/ZK1_fast_force_kernel/x48_fast.py --mass $1 --seed $2 --ng $3 --work $W --resume >> $W/run.log 2>&1; }
pids=()
trap 'kill -TERM "${pids[@]}" 2>/dev/null; wait; exit 75' TERM INT
for m in 1e10 1e11; do
  for s in 1 2 3 4 5 6 7 8 9; do run $m $s 64 & pids+=($!); done
  for s in 1 2 3; do run $m $s 48 & pids+=($!); done
done
wait
echo "X80 runs finished"
