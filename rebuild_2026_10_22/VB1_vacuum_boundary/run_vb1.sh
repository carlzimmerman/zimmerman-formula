#!/bin/bash
# VB1: Argon's door D2. Two same-seed 1e14 runs at ng 48: A (--rs 1.5, control) and B (--rs 2.0, the IC grid's ceiling),
# each collapsed with x48_fast.py then continued to z = 0 with zn1_continue.py, unchanged. Starts only after ZN4's 12
# runs and the nine 1e12 ng 80 seeds have written done.json, and only while the 1-minute load is under 8. Single thread,
# nice 15, --resume; SIGTERM -> checkpoint, exit 75. After a restart re-run. Criteria: FROZEN_CRITERIA.md (committed first).
cd "$(dirname "$0")/../.."
V=rebuild_2026_10_22/VB1_vacuum_boundary; K=rebuild_2026_10_22/ZK1_fast_force_kernel/x48_fast.py; C=rebuild_2026_10_22/ZN1_zooms_to_z0/zn1_continue.py
need() { for m in 1e14 1e15; do for s in 1 2 3 4 5 6; do [ -f rebuild_2026_10_22/ZN4_cluster_resolution/runs/M${m}_s${s}_ng80/done.json ] || return 1; done; done
         for s in 1 2 3 4 5 6 7 8 9; do [ -f rebuild_2026_10_22/X48_native_cf_zoom/runs/M1e12_s${s}_ng80/done.json ] || return 1; done
         [ ! -f compute_queue/YIELD_VB1 ]; }
until need; do sleep 600; done
until [ "$(sysctl -n vm.loadavg | awk '{print int($2)}')" -lt 8 ]; do sleep 300; done
run() { D=M1e14_s1_ng48_rs$1; A=$V/runs_zf/$D; B=$V/runs/$D; mkdir -p $A $B; touch $A/ZK1_SWITCHED $B/ZK1_SWITCHED; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
  [ -f $A/done.json ] || nice -n 15 python3 $K --mass 1e14 --seed 1 --ng 48 --rs $1 --work $A --resume >> $A/run.log 2>&1
  [ -f $A/done.json ] && exec nice -n 15 python3 $C --src $A --work $B --resume >> $B/run.log 2>&1; }
pids=(); trap 'kill -TERM "${pids[@]}" 2>/dev/null; wait; exit 75' TERM INT
for rs in 1.5 2.0; do run $rs & pids+=($!); done
wait; echo "VB1 runs finished $(date)"
