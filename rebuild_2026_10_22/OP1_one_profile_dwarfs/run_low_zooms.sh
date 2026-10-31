#!/bin/bash
# OP1: 1e9, 1e8 zooms, seeds 1-9, ng 64, to z_f then z = 0 (ZN1's continuation). Waits until the ng 80 batch and its continuations have gone, two checks running. Single thread, nice 15; --resume continues; SIGTERM -> children checkpoint, exit 75. After a restart re-run this script. Writes LOW_ZOOMS_DONE.
cd "$(dirname "$0")/../.."
O=rebuild_2026_10_22/OP1_one_profile_dwarfs; K=rebuild_2026_10_22/ZK1_fast_force_kernel/x48_fast.py; C=rebuild_2026_10_22/ZN1_zooms_to_z0/zn1_continue.py
n=0; until [ $n -ge 2 ]; do if pgrep -f 'ng 80|zn1_continue.py' >/dev/null; then n=0; else n=$((n+1)); fi; sleep 300; done
run() { A=$O/runs_zf/M$1_s$2_ng64; W=$O/runs/M$1_s$2_ng64; mkdir -p $A $W; touch $A/ZK1_SWITCHED $W/ZK1_SWITCHED; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
  [ -f $A/done.json ] || nice -n 15 python3 $K --mass $1 --seed $2 --ng 64 --work $A --resume >> $A/run.log 2>&1 || return; nice -n 15 python3 $C --src $A --work $W --resume >> $W/run.log 2>&1; }
pids=(); trap 'kill -TERM "${pids[@]}" 2>/dev/null; pkill -TERM -f "$O/runs" ; wait; exit 75' TERM INT
for m in 1e9 1e8; do for s in 1 2 3 4 5 6 7 8 9; do run $m $s & pids+=($!); done; done
wait
[ "$(ls $O/runs/M1e[89]_s?_ng64/done.json 2>/dev/null | wc -l | tr -d ' ')" -ge 18 ] && touch $O/LOW_ZOOMS_DONE; echo "OP1 low zooms finished $(date)"
