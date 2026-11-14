#!/bin/bash
# XJ1 build B runner (FROZEN_CRITERIA.md ef8ccdde98, section 3; FWN1R's run_all.sh with the driver's name changed):
# primary seeds 0 to 3 in all 12 bins, then brackets (anchors, seeds 0, 1, one process per bracket). Two copies may run
# at once (exclusive claim files). The driver checks before every part: STOP (exit 2) below 8 GB disk or above 14 GB swap;
# WAIT (exit 3) unless >= 10 GB disk and >= 24 GB free + inactive memory.
# Usage: run_b.sh <tag>
cd "$(dirname "$0")"
echo $$ > logs/run_b_$1.pid
for st in "prim 0 1 2 3" "br"; do
  for i in $(seq 1 900); do
    nice -n 19 python3 -I -B xj1b_run.py $st; rc=$?
    [ $rc -eq 0 ] && break
    [ $rc -eq 3 ] && { sleep 60; continue; }
    [ $rc -ne 75 ] && { echo "stage $st exited $rc"; exit $rc; }
  done
done
touch run_b_$1.done
