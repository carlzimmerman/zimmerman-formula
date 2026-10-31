#!/bin/bash
# X48 A4's last zooms, resumed from their numpy checkpoints with ZK1's kernel (AMENDMENT_ZK1.md). 4 threads each. SIGTERM -> checkpoint, exit 75.
cd "$(dirname "$0")/../.."
L=rebuild_2026_10_22/X48_native_cf_zoom
run() { W=$L/runs/M1e13_s$1_ng64; touch $W/ZK1_SWITCHED; ZK1_THREADS=4 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 exec nice -n 15 python3 rebuild_2026_10_22/ZK1_fast_force_kernel/x48_fast.py --mass 1e13 --seed $1 --ng 64 --work $W --resume >> $W/run.log 2>&1; }
pids=(); trap 'kill -TERM "${pids[@]}" 2>/dev/null; wait; exit 75' TERM INT
for s in "$@"; do run $s & pids+=($!); done
wait; echo "A4 last zooms finished $(date)"
