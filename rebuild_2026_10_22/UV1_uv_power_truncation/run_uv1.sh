#!/bin/bash
# UV1: 1e14, seeds 1-9, ng 64; kick and cut variants, each to z_f then on to z = 0. Starts once LC1's discs have finished. Single thread, nice 15; --resume continues; SIGTERM -> children checkpoint, exit 75. After a restart re-run this script.
cd "$(dirname "$0")/../.."
U=rebuild_2026_10_22/UV1_uv_power_truncation; C=rebuild_2026_10_22/ZN1_zooms_to_z0/zn1_continue.py; LC=rebuild_2026_10_22/LC1_live_contraction/runs
until [ "$(ls $LC/*/done.json 2>/dev/null | wc -l | tr -d ' ')" -ge 10 ]; do sleep 60; done
KICK=$(python3 -c "import json;print(json.load(open('$U/uv1_setup.json'))['kick'])"); KCUT=$(python3 -c "import json;print(json.load(open('$U/uv1_setup.json'))['kcut'])")
run() { V=$1; S=$2; D=${V}_s${S}; A=$U/runs_zf/$D; B=$U/runs/$D; mkdir -p $A $B; touch $A/ZK1_SWITCHED $B/ZK1_SWITCHED; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
  if [ ! -f $A/done.json ]; then if [ "$V" = kick ]; then UV1_KICK=$KICK nice -n 15 python3 $U/uv1_zoom.py --mass 1e14 --seed $S --ng 64 --work $A --resume >> $A/run.log 2>&1; else UV1_KCUT=$KCUT nice -n 15 python3 $U/uv1_zoom.py --mass 1e14 --seed $S --ng 64 --work $A --resume >> $A/run.log 2>&1; fi; fi
  [ -f $A/done.json ] && exec nice -n 15 python3 $C --src $A --work $B --resume >> $B/run.log 2>&1; }
pids=(); trap 'kill -TERM "${pids[@]}" 2>/dev/null; wait; exit 75' TERM INT
for v in kick cut; do for s in 1 2 3 4 5 6 7 8 9; do run $v $s & pids+=($!); done; done
wait; echo "UV1 runs finished $(date)"
