#!/bin/bash
# X48 A4: 18 ng 64 seeds at 1e13 and 1e14, all concurrently (single thread each, nice 15); --resume continues from any checkpoint; SIGTERM -> children checkpoint, exit 75
cd "$(dirname "$0")/../.."
L=rebuild_2026_10_22/X48_native_cf_zoom
run() { W=$L/runs/M$1_s$2_ng64; mkdir -p $W; OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 15 python3 $L/x48_zoom.py --mass $1 --seed $2 --ng 64 --work $W --resume >> $W/run.log 2>&1; }
pids=()
trap 'kill -TERM "${pids[@]}" 2>/dev/null; wait; exit 75' TERM INT
for m in 1e13 1e14; do for s in 1 2 3 4 5 6 7 8 9; do run $m $s & pids+=($!); done; done
wait
echo "A4 finished"
