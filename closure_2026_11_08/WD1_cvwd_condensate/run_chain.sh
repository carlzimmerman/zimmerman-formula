#!/bin/bash
# WD1 compute chain: one child at a time, nice 10, df check before each (stop under 2 GiB free).
# WD1_PJ1_DIR: a read-only copy of origin/main's PJ1 lane directory when the shared checkout is behind origin (default: the repo's own path).
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1
check() { free=$(df -g . | tail -1 | awk '{print $4}'); echo "[chain] df free ${free} GiB before $1"; if [ "$free" -lt 2 ]; then echo "[chain] STOP: under 2 GiB free before $1"; exit 3; fi; }
check ka; nice -n 10 python3 wd1.py ka > run_ka.txt 2>&1 || exit 1
check local; nice -n 10 python3 wd1.py local > run_local.txt 2>&1 || exit 1
check M1; WD1_MUTATE=M1 nice -n 10 python3 wd1.py local > run_local_M1.txt 2>&1 || exit 1
check M2; WD1_MUTATE=M2 nice -n 10 python3 wd1.py local > run_local_M2.txt 2>&1 || exit 1
check M3; WD1_MUTATE=M3 nice -n 10 python3 wd1.py local > run_local_M3.txt 2>&1 || exit 1
check bullet; nice -n 10 python3 wd1.py bullet > run_bullet.txt 2>&1 || exit 1
check cmb_canonical; WD1_FOOT=canonical WD1_REFIT_FEV=100 nice -n 10 python3 wd1_cmb.py > run_cmb_canonical.txt 2>&1 || exit 1
check cmb_alt; WD1_FOOT=alt WD1_REFIT_FEV=100 nice -n 10 python3 wd1_cmb.py > run_cmb_alt.txt 2>&1 || exit 1
check web; nice -n 10 python3 wd1_web.py > run_web.txt 2>&1 || exit 1
check grade; python3 wd1_grade.py > /dev/null || exit 1
echo "[chain] done"
