#!/bin/bash
# FRZ6R resume (lead's operational rule of 21:22; same frozen parts, seeds and brackets). The driver checks before each part:
# STOP (exit 2) below 8 GB free disk or above 14 GB swap used; WAIT (exit 3) unless >= 10 GB disk and >= 24 GB free + inactive memory.
# Usage: run_resume.sh <tag>; two runners may share the plan (exclusive claim files).
cd "$(dirname "$0")"
for st in "prim 0 1 2" "prim 3" "br"; do
  for i in $(seq 1 600); do
    nice -n 19 python3 -I -B frz6r_run.py $st; rc=$?
    [ $rc -eq 0 ] && break
    [ $rc -eq 3 ] && { sleep 60; continue; }
    [ $rc -ne 75 ] && { echo "stage $st exited $rc"; exit $rc; }
  done
done
touch run_resume_$1.done
