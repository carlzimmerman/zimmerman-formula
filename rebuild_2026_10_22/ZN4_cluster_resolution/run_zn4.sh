#!/bin/bash
# ZN4: ng 80, seeds 1-6 at 1e14, 1e15, after ZN2's low-mass runs. Single thread, nice 15; --resume; SIGTERM -> checkpoint, exit 75. After a restart re-run.
cd "$(dirname "$0")/../.."
Z=rebuild_2026_10_22/ZN4_cluster_resolution; K=rebuild_2026_10_22/ZK1_fast_force_kernel/x48_fast.py; C=rebuild_2026_10_22/ZN1_zooms_to_z0/zn1_continue.py
until [ -f rebuild_2026_10_22/ZN2_native_profile_sparc_groups/LOW_Z0_DONE ]; do sleep 300; done
run() { D=M$1_s$2_ng80; A=$Z/runs_zf/$D; B=$Z/runs/$D; mkdir -p $A $B; touch $A/ZK1_SWITCHED $B/ZK1_SWITCHED; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
  [ -f $A/done.json ] || nice -n 15 python3 $K --mass $1 --seed $2 --ng 80 --work $A --resume >> $A/run.log 2>&1
  [ -f $A/done.json ] && exec nice -n 15 python3 $C --src $A --work $B --resume >> $B/run.log 2>&1; }
pids=(); trap 'kill -TERM "${pids[@]}" 2>/dev/null; wait; exit 75' TERM INT
for m in 1e14 1e15; do for s in 1 2 3 4 5 6; do run $m $s & pids+=($!); done; done
wait; echo "ZN4 finished $(date)"
