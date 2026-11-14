#!/bin/bash
# FRZ6R second runner (lead's operational change, 2026-11-13): the same frozen parts and seeds as run_all.sh, taken from the
# other end of the plan (S2 seed 3, then S3 brackets); parts are claimed exclusively, so each part is computed once.
cd "$(dirname "$0")"
for st in "prim 3" "br"; do
  for i in $(seq 1 300); do
    nice -n 19 python3 -I -B frz6r_run.py $st; rc=$?
    [ $rc -eq 0 ] && break
    [ $rc -ne 75 ] && { echo "stage $st exited $rc"; exit $rc; }
  done
done
touch run_lane2.done
