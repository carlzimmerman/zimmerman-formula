#!/bin/bash
# ZN3: 1e15, seeds 1-9, ng 64: X48's zoom with ZK1's kernel to z_f, then ZN1's continuation to z = 0. Single thread, nice 15; --resume continues; SIGTERM -> children checkpoint, exit 75. After a restart re-run this script.
cd "$(dirname "$0")/../.."
Z=rebuild_2026_10_22/ZN3_native_shape_at_1e15; K=rebuild_2026_10_22/ZK1_fast_force_kernel/x48_fast.py; C=rebuild_2026_10_22/ZN1_zooms_to_z0/zn1_continue.py
run() { D=M1e15_s$1_ng64; A=$Z/runs_zf/$D; B=$Z/runs/$D; mkdir -p $A $B; touch $A/ZK1_SWITCHED $B/ZK1_SWITCHED; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
  [ -f $A/done.json ] || nice -n 15 python3 $K --mass 1e15 --seed $1 --ng 64 --work $A --resume >> $A/run.log 2>&1
  [ -f $A/done.json ] && exec nice -n 15 python3 $C --src $A --work $B --resume >> $B/run.log 2>&1; }
pids=(); trap 'kill -TERM "${pids[@]}" 2>/dev/null; wait; exit 75' TERM INT
for s in 1 2 3 4 5 6 7 8 9; do run $s & pids+=($!); done
wait; echo "ZN3 runs finished $(date)"
