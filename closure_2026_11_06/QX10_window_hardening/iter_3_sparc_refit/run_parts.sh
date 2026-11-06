#!/bin/bash
# runs iter_3 parts two at a time, each waiting while the 1-min load average is above 45
cd "$(dirname "$0")"
waitload(){ while [ "$(sysctl -n vm.loadavg | awk '{print int($2)}')" -gt 45 ]; do sleep 60; done; }
for pair in "C1 C2" "C3 C4" "MUTATE"; do
  waitload
  for c in $pair; do OMP_NUM_THREADS=1 nice -n 15 python3 qx10_i3.py $c > log_$c.txt 2>&1 & done
  wait
done
echo ALLDONE
