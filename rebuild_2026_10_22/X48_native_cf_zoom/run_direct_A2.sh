#!/bin/bash
# X48 A2: 18 more ng 48 seeds, 9 at a time (single thread each, nice 15); --resume continues from any checkpoint
cd "$(dirname "$0")/../.."
L=rebuild_2026_10_22/X48_native_cf_zoom
run() { W=$L/runs/M$1_s$2_ng48; mkdir -p $W; OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 15 python3 $L/x48_zoom.py --mass $1 --seed $2 --ng 48 --work $W --resume >> $W/run.log 2>&1; }
pids=()
trap 'kill -TERM "${pids[@]}" 2>/dev/null; wait; exit 75' TERM INT
for wave in "4 5 6" "7 8 9"; do
  pids=()
  for s in $wave; do for m in 1e12 1e13 1e14; do run $m $s & pids+=($!); done; done
  wait
done
echo "A2 finished"
