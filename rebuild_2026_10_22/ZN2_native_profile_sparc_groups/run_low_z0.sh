#!/bin/bash
# ZN2 A1: X80's ng 64 seeds at 1e10, 1e11 continued to z = 0, starting once LC1's discs have finished. Single thread, nice 15; --resume continues; SIGTERM -> children checkpoint, exit 75. After a restart re-run this script. Writes LOW_Z0_DONE when all 18 have finished.
cd "$(dirname "$0")/../.."
Z=rebuild_2026_10_22/ZN2_native_profile_sparc_groups; X=rebuild_2026_10_22/X48_native_cf_zoom/runs; C=rebuild_2026_10_22/ZN1_zooms_to_z0/zn1_continue.py; LC=rebuild_2026_10_22/LC1_live_contraction/runs
until [ "$(ls $LC/*/done.json 2>/dev/null | wc -l | tr -d ' ')" -ge 10 ]; do sleep 60; done
run() { D=M$1_s$2_ng64; W=$Z/runs/$D; mkdir -p $W; touch $W/ZK1_SWITCHED; OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 exec nice -n 15 python3 $C --src $X/$D --work $W --resume >> $W/run.log 2>&1; }
pids=(); trap 'kill -TERM "${pids[@]}" 2>/dev/null; wait; exit 75' TERM INT
for m in 1e11 1e10; do for s in 1 2 3 4 5 6 7 8 9; do run $m $s & pids+=($!); done; done
wait
[ "$(ls $Z/runs/M1e1[01]_s?_ng64/done.json 2>/dev/null | wc -l | tr -d ' ')" -ge 18 ] && touch $Z/LOW_Z0_DONE; echo "ZN2 low-mass runs finished $(date)"
