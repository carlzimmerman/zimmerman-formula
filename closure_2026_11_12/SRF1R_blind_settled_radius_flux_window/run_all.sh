#!/bin/bash
# SRF1R stage 1 queue (READING cc3d45432d, A1 696d184fbf, A2 23c3b8956a): one job at a time, nice 19, 4 workers.
# Parts already written are skipped (restartable). Writes run_all.done at the end.
cd "$(dirname "$0")"
run() { nice -n 19 python3 srf1r_flux.py "$@" >> logs/run_all.log 2>&1; rc=$?; if [ $rc -eq 75 ]; then echo "stopped" >> logs/run_all.log; exit 75; fi; }
for z in 2.2 3.0 4.4; do run P both $z 0; done
for z in 2.4 2.6 2.8 3.2 3.4 3.6 3.8 4.0 4.2; do run P both $z 0; done
for s in 1 2; do for z in 2.2 3.0 4.4; do run P both $z $s; done; done
for z in 2.2 3.0 4.4; do run M1 both $z 0; run M2 both $z 0; done
for b in B1 B2 B3 B4 B5 B6 B7 B8 B9 B10; do for z in 2.2 3.0 4.4; do run $b both $z 0; done; done
date > run_all.done
