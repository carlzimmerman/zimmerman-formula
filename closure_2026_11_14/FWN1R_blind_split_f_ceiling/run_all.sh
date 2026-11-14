#!/bin/bash
# FWN1R runner (FROZEN_CRITERIA.md, ed67b21129): primary seeds 0 to 3 in all 12 bins, then brackets (anchors, seeds 0, 1, one
# process per bracket). Two copies may run at once (exclusive claim files). The driver checks before every part: STOP (exit 2)
# below 8 GB disk or above 14 GB swap; WAIT (exit 3) unless >= 10 GB disk and >= 24 GB free + inactive memory.
# Usage: run_all.sh <tag>
cd "$(dirname "$0")"
for st in "prim 0 1 2 3" "br"; do
  for i in $(seq 1 600); do
    nice -n 19 python3 -I -B fwn1r_run.py $st; rc=$?
    [ $rc -eq 0 ] && break
    [ $rc -eq 3 ] && { sleep 60; continue; }
    [ $rc -ne 75 ] && { echo "stage $st exited $rc"; exit $rc; }
  done
done
touch run_all_$1.done
