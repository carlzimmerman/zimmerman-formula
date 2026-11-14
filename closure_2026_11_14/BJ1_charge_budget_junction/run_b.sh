#!/bin/bash
# BJ1 build B runner (FROZEN_CRITERIA.md 9e7ce0dfe6, section 2, G-F at flux level): XJ1's run_b2.sh
# (closure_2026_11_14/XJ1_exact_junction_zero_velocity_surface) with the driver's name changed and the other lanes' heavy
# drivers named in the wait: a part starts only when no more than BJ1_MAXOTHER (default two) other heavy part processes
# are alive (the criteria: "only when no more than two other heavy processes are alive"). Primary seeds 0 to 3 in all 12
# bins, then brackets (anchors, seeds 0, 1, one process per part). Two copies may run at once (exclusive claim files).
# The driver checks before every part: STOP (exit 2) below 8 GB disk or above 14 GB swap; WAIT (exit 3) unless >= 10 GB
# disk and >= 24 GB free + inactive memory. The graded fields follow BJ1B_CASES (default B1,B2,B3).
# Usage: run_b.sh <tag>
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
cd "$(dirname "$0")"
mkdir -p logs
echo $$ > logs/run_b_$1.pid
for st in "prim 0 1 2 3" "br"; do
  for i in $(seq 1 900); do
    while [ "$(pgrep -f 'fwn2a_run.py|fwn2b_run.py|xj1b_run.py|xj1a_run.py|xj1b2_run.py|wlj2_lwb.py' | wc -l)" -gt "${BJ1_MAXOTHER:-2}" ]; do sleep 30; done
    nice -n 19 python3 -I -B bj1b_run.py $st; rc=$?
    [ $rc -eq 0 ] && break
    [ $rc -eq 3 ] && { sleep 60; continue; }
    [ $rc -ne 75 ] && { echo "stage $st exited $rc"; exit $rc; }
  done
done
touch run_b_$1.done
