#!/bin/bash
# ZN1 with ZK1's kernel: seeds 1-9 at 1e12, 1e13, 1e14, ng 64, each starting once X48's done.json exists; single thread, nice 15; --resume continues from any checkpoint; SIGTERM -> children checkpoint, exit 75. After a restart re-run this script.
cd "$(dirname "$0")/../.."
L=rebuild_2026_10_22/ZN1_zooms_to_z0; X=rebuild_2026_10_22/X48_native_cf_zoom/runs
run() { D=M$1_s$2_ng64; W=$L/runs/$D; mkdir -p $W; until [ -f $X/$D/done.json ]; do sleep 30; done; touch $W/ZK1_SWITCHED
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 exec nice -n 15 python3 $L/zn1_continue.py --src $X/$D --work $W --resume >> $W/run.log 2>&1; }
pids=(); trap 'kill -TERM "${pids[@]}" 2>/dev/null; wait; exit 75' TERM INT
for m in 1e13 1e14 1e12; do for s in 1 2 3 4 5 6 7 8 9; do run $m $s & pids+=($!); done; done
wait; echo "ZN1 runs finished $(date)"
