#!/bin/bash
# TS1 cosmology chain: one CLASS process at a time, nice 10, stop under 2 GiB free.
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1
check() { free=$(df -g . | tail -1 | awk '{print $4}'); if [ "$free" -lt 2 ]; then echo "[chain] STOP"; exit 3; fi; }
check; nice -n 10 python3 ts1_cosmo.py cosmo MW alt > run_cosmo_MW_alt.txt 2>&1 || echo "FAILED cosmo MW alt"
for f in canonical alt; do check; nice -n 10 python3 ts1_cosmo.py cosmo MSPLIT $f > run_cosmo_MSPLIT_$f.txt 2>&1 || echo "FAILED cosmo MSPLIT $f"; done
for v in MW MSPLIT; do for f in canonical alt; do check; nice -n 10 python3 ts1_cosmo.py seed $v $f > run_seed_${v}_$f.txt 2>&1 || echo "FAILED seed $v $f"; done; done
check; nice -n 10 python3 ts1_cosmo.py hc1 MSPLIT > run_g9_MSPLIT.txt 2>&1 || echo "FAILED g9"
for f in canonical alt; do check; nice -n 10 python3 ts1_cosmo.py cmb MSPLIT $f > run_cmb7a_MSPLIT_$f.txt 2>&1 || echo "FAILED cmb $f"; done
echo "[chain] done"
