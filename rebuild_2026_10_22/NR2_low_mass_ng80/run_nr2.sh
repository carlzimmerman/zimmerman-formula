#!/bin/bash
# NR2: 1e10, 1e11, seeds 1-9, ng 80, to z_f with ZK1's kernel; single thread, nice 15; --resume continues; SIGTERM -> children checkpoint, exit 75. After a restart re-run this script.
cd "$(dirname "$0")/../.."
L=rebuild_2026_10_22/NR2_low_mass_ng80
run() { W=$L/runs/M$1_s$2_ng80; mkdir -p $W; touch $W/ZK1_SWITCHED; OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/ZK1_fast_force_kernel/x48_fast.py --mass $1 --seed $2 --ng 80 --work $W --resume >> $W/run.log 2>&1; }
pids=(); trap 'kill -TERM "${pids[@]}" 2>/dev/null; wait; exit 75' TERM INT
for m in 1e10 1e11; do for s in 1 2 3 4 5 6 7 8 9; do run $m $s & pids+=($!); done; done
wait; echo "NR2 runs finished $(date)"
