#!/bin/bash
# SS1 variants B-G chain (AMENDMENT_A2 / A3): one child at a time, nice 10, df check (stop under 2 GiB free).
# SS1_PJ1_DIR: a read-only copy of origin/main's PJ1 lane directory when the shared checkout is behind origin.
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1
check() { free=$(df -g . | tail -1 | awk '{print $4}'); echo "[chain] df free ${free} GiB before $1"; if [ "$free" -lt 2 ]; then echo "[chain] STOP: under 2 GiB free"; exit 3; fi; }
run() { check "$*"; nice -n 10 python3 ss1v.py "$@" > "run_v_$(echo "$*${SS1V_OPT:+_$SS1V_OPT}${SS1_FOOT:+_$SS1_FOOT}${SS1V_FCEN:+_fcen$SS1V_FCEN}" | tr ' ' '_').txt" 2>&1 || echo "[chain] FAILED $*"; }
run ka
for V in G B C D E F; do
  run local $V
  for f in canonical alt; do SS1_FOOT=$f run cosmo $V; done
  run bullet $V
done
SS1V_OPT=obs run local G
SS1V_OPT=local run local G
SS1V_FCEN=0.3 run local F
for V in MG1 MG2 MG3 MG4; do run local $V; for f in canonical alt; do SS1_FOOT=$f run cosmo $V; done; run bullet $V; done
echo "[chain] done"
