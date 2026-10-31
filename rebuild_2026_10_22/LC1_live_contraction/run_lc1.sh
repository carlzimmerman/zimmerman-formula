#!/bin/bash
# LC1: seeds 1-9 at 1e12, ng 64, a disc grown from z_f to z = 0; plus one MUTATE seed with M_d x 2. Single thread, nice 15; --resume continues; SIGTERM -> checkpoint, exit 75. After a restart re-run this script.
cd "$(dirname "$0")/../.."
L=rebuild_2026_10_22/LC1_live_contraction
run() { W=$L/runs/$1; mkdir -p $W; OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 exec nice -n 15 python3 $L/lc1_disc.py --seed $2 --work $W --resume --md-mult $3 >> $W/run.log 2>&1; }
pids=(); trap 'kill -TERM "${pids[@]}" 2>/dev/null; wait; exit 75' TERM INT
for s in 1 2 3 4 5 6 7 8 9; do run M1e12_s${s}_ng64 $s 1 & pids+=($!); done
run M1e12_s1_ng64_MUTATE 1 2 & pids+=($!)
wait; echo "LC1 runs finished $(date)"
