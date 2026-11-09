#!/bin/bash
# SS4 chain: one child at a time, nice 10, df check (stop under 2 GiB free). SS1_PJ1_DIR: read-only copy of origin's PJ1 lane dir.
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1
check() { free=$(df -g . | tail -1 | awk '{print $4}'); if [ "$free" -lt 2 ]; then echo "[chain] STOP"; exit 3; fi; }
check; nice -n 10 python3 ss4.py optc > run_optc.txt 2>&1 || echo "FAILED optc"
for V in Kp2 Kform MK1 MK2; do check; nice -n 10 python3 ss4.py local $V > run_local_$V.txt 2>&1 || echo "FAILED local $V"; done
check; nice -n 10 python3 ss4.py bullet K > run_bullet_K.txt 2>&1 || echo "FAILED bullet"
for V in K Kform MK2; do for f in canonical alt; do check; SS4_V=$V SS1_FOOT=$f nice -n 10 python3 ss4_cosmo.py > run_cosmo_${V}_$f.txt 2>&1 || echo "FAILED cosmo $V $f"; done; done
echo "[chain] done"
