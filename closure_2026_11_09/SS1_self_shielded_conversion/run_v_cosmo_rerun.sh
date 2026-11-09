#!/bin/bash
# rerun of the C-G cosmology after the streaming-length unit fix (km/s x Gyr = kpc), plus the M_min 1e10 bracket.
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1
for V in G C D E F; do for f in canonical alt; do SS1_FOOT=$f nice -n 10 python3 ss1v.py cosmo $V > run_v_cosmo_${V}_${f}.txt 2>&1; done; done
for V in G B C D E F; do for f in canonical alt; do SS1V_MMIN=1e10 SS1_FOOT=$f nice -n 10 python3 ss1v.py cosmo $V > run_v_cosmo_${V}_${f}_mmin1e10.txt 2>&1; done; done
echo done
