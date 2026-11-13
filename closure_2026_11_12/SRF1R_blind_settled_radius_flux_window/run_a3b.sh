#!/bin/bash
# SRF1R queue after AMENDMENT A3, restarted: one footing per process (a pool forked after the first footing's FFT threads
# deadlocked once). One job at a time, nice 19, 4 workers; restartable; run_a3.done at the end.
cd "$(dirname "$0")"
run() { for ft in canonical alt; do nice -n 19 python3 srf1r_flux.py "$1" $ft "$2" "$3" >> logs/run_all.log 2>&1; [ $? -eq 75 ] && exit 75; done; }
run P 4.4 0
run M1 2.2 0; run M2 2.2 0
run P 2.2 1
for b in B2 B3 B8 B1 B4 B5 B6 B7 B9 B10; do run $b 2.2 0; done
date > run_a3.done
