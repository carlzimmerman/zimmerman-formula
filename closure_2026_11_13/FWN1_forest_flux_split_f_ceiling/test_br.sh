#!/bin/bash
# FWN1: second test of the first bracket part: resume it until its first forced box is written, then SIGTERM.
cd "$(dirname "$0")"
export FWN1_THREADS=3 FWN1_MEM_GB=16
tag=bracketF_z2.2_s0_canonical
while true; do
  nice -n 19 python3 -I -B fwn1_run.py bracketF 2.2 0 canonical & pid=$!
  while kill -0 $pid 2>/dev/null; do
    if ls tmp/$tag/b0*.json >/dev/null 2>&1; then kill -TERM $pid; break; fi
    sleep 5
  done
  wait $pid; rc=$?; echo "rc $rc ($(date +%H:%M)): $(ls tmp/$tag | tr '\n' ' ')"
  [ $rc -eq 76 ] && ! ls tmp/$tag/b0*.json >/dev/null 2>&1 && continue
  break
done
