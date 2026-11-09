#!/bin/bash
# WM1 cosmology chain: one CLASS process at a time, nice 10, stop under 2 GiB free.
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1
check() { free=$(df -g . | tail -1 | awk '{print $4}'); if [ "$free" -lt 2 ]; then echo "[chain] STOP"; exit 3; fi; }
check; WM1_V=W SS1_FOOT=alt nice -n 10 python3 wm1_cosmo.py > run_cosmo_W_alt.txt 2>&1 || echo "FAILED cosmo W alt"
for M in W MW1 MW2 W3 Wthird; do check; nice -n 10 python3 wm1_hc1.py $M > run_g9_$M.txt 2>&1 || echo "FAILED g9 $M"; done
for V in MW1 MW2 W3 Wthird; do for f in canonical alt; do check; WM1_V=$V SS1_FOOT=$f nice -n 10 python3 wm1_cosmo.py > run_cosmo_${V}_$f.txt 2>&1 || echo "FAILED cosmo $V $f"; done; done
for f in canonical alt; do check; SS1_FOOT=$f nice -n 10 python3 wm1_cmb.py > run_cmb7a_$f.txt 2>&1 || echo "FAILED cmb7a $f"; done
echo "[chain] done"
