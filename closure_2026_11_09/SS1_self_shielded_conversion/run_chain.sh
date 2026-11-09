#!/bin/bash
# SS1 compute chain: one child at a time, nice 10, df check before each (stop under 2 GiB free).
# SS1_PJ1_DIR: a read-only copy of origin/main's PJ1 lane directory when the shared checkout is behind origin.
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1
check() { free=$(df -g . | tail -1 | awk '{print $4}'); echo "[chain] df free ${free} GiB before $1"; if [ "$free" -lt 2 ]; then echo "[chain] STOP: under 2 GiB free before $1"; exit 3; fi; }
check core; nice -n 10 python3 ss1.py core > run_core.txt 2>&1 || exit 1
check local; nice -n 10 python3 ss1.py local > run_local.txt 2>&1 || exit 1
for f in canonical alt; do check cosmo_$f; SS1_FOOT=$f nice -n 10 python3 ss1_cosmo.py > run_cosmo_$f.txt 2>&1 || exit 1; done
check bullet; nice -n 10 python3 ss1_bullet.py > run_bullet.txt 2>&1 || exit 1
for m in M1 M2 M3 M4; do
  check local_$m; SS1_MUTATE=$m nice -n 10 python3 ss1.py local > run_local_$m.txt 2>&1 || exit 1
  for f in canonical alt; do check cosmo_${f}_$m; SS1_MUTATE=$m SS1_FOOT=$f nice -n 10 python3 ss1_cosmo.py > run_cosmo_${f}_$m.txt 2>&1 || exit 1; done
  check bullet_$m; SS1_MUTATE=$m nice -n 10 python3 ss1_bullet.py > run_bullet_$m.txt 2>&1 || exit 1
done
echo "[chain] done"
