#!/bin/bash
# SRF1R queue after AMENDMENT A3 (f845b9632f): one job at a time, nice 19, 4 workers; restartable; run_a3.done at the end.
cd "$(dirname "$0")"
while kill -0 75233 2>/dev/null; do sleep 20; done          # the running z 2.2 seed 0 part (both footings)
run() { nice -n 19 python3 srf1r_flux.py "$@" >> logs/run_all.log 2>&1; [ $? -eq 75 ] && exit 75; }
run P both 2.2 0
for z in 3.0 4.4; do run P both $z 0; done
run M1 both 2.2 0; run M2 both 2.2 0
run P both 2.2 1
for b in B2 B3 B8 B1 B4 B5 B6 B7 B9 B10; do run $b both 2.2 0; done
date > run_a3.done
