#!/bin/bash
# fsigma8 derivative fix (fine low-z grid, A4 disclosure): rerun every variant cosmology in SS1 (B-H, MG, MH, M_min 1e10) and SS2 (G).
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1
check() { free=$(df -g . | tail -1 | awk '{print $4}'); if [ "$free" -lt 2 ]; then echo "[chain] STOP"; exit 3; fi; }
for V in H Hfull Hsrc MH1 MH2; do for f in canonical alt; do check; SS1_FOOT=$f nice -n 10 python3 ss1v.py cosmo $V > run_h_cosmo_${V}_$f.txt 2>&1 || echo "FAILED $V $f"; done; done
check; nice -n 10 python3 ss1v.py local MH1 > run_h_local_MH1.txt 2>&1 || echo "FAILED local MH1"
for V in G B C D E F MG1 MG2 MG3 MG4; do for f in canonical alt; do check; SS1_FOOT=$f nice -n 10 python3 ss1v.py cosmo $V > run_v_cosmo_${V}_$f.txt 2>&1 || echo "FAILED $V $f"; done; done
for V in G B C D E F; do for f in canonical alt; do check; SS1V_MMIN=1e10 SS1_FOOT=$f nice -n 10 python3 ss1v.py cosmo $V > run_v_cosmo_${V}_${f}_mmin1e10.txt 2>&1 || echo "FAILED mmin $V $f"; done; done
cd ../SS2_virial_gated_conversion
for V in G Gsrc MG1 MG2 MG3 MG4 Gz2; do for f in canonical alt; do check; SS1_FOOT=$f nice -n 10 python3 ss2.py cosmo $V > run_cosmo_${V}_$f.txt 2>&1 || echo "FAILED ss2 $V $f"; done; done
for f in canonical alt; do check; SS1V_MMIN=1e10 SS1_FOOT=$f nice -n 10 python3 ss2.py cosmo G > run_cosmo_G_${f}_mmin1e10.txt 2>&1 || echo "FAILED ss2 mmin $f"; done
echo "[chain] done"
