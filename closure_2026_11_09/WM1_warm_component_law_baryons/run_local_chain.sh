#!/bin/bash
# WM1 local chain: one child at a time, nice 10, stop under 2 GiB free. SS1_PJ1_DIR: read-only extract of origin's PJ1 lane dir (set by caller).
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1
check() { free=$(df -g . | tail -1 | awk '{print $4}'); if [ "$free" -lt 2 ]; then echo "[chain] STOP"; exit 3; fi; }
for V in W3 Wthird MW1 MW2 Racc; do check; nice -n 10 python3 wm1_local.py local $V > run_local_$V.txt 2>&1 || echo "FAILED local $V"; done
for V in W MW1 MW2 Racc; do check; nice -n 10 python3 wm1_local.py bullet $V > run_bullet_$V.txt 2>&1 || echo "FAILED bullet $V"; done
echo "[chain] done"
