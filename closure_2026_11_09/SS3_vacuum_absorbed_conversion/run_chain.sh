#!/bin/bash
# SS3 chain: one child at a time, nice 10, df check (stop under 2 GiB free). SS1_PJ1_DIR: read-only copy of origin's PJ1 lane dir.
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1
check() { free=$(df -g . | tail -1 | awk '{print $4}'); if [ "$free" -lt 2 ]; then echo "[chain] STOP"; exit 3; fi; }
check; nice -n 10 python3 ss3.py ka > run_ka.txt 2>&1 || echo "FAILED ka"
for V in J Jsrc J_NFW MJ2; do check; nice -n 10 python3 ss3.py local $V > run_local_$V.txt 2>&1 || echo "FAILED local $V"; done
check; nice -n 10 python3 ss3.py bullet J > run_bullet_J.txt 2>&1 || echo "FAILED bullet"
for f in canonical alt; do
  check; SS1_FOOT=$f nice -n 10 python3 ss3_cosmo.py > run_cosmo_J_$f.txt 2>&1 || echo "FAILED cosmo J $f"
  check; SS3_MMIN=2e11 SS1_FOOT=$f nice -n 10 python3 ss3_cosmo.py > run_cosmo_J_mmin2e11_$f.txt 2>&1 || echo "FAILED mmin $f"
  check; SS3_W=0.3333333333 SS1_FOOT=$f nice -n 10 python3 ss3_cosmo.py > run_cosmo_MJ1_$f.txt 2>&1 || echo "FAILED MJ1 $f"
  check; SS3_V=MJ2 SS1_FOOT=$f nice -n 10 python3 ss3_cosmo.py > run_cosmo_MJ2_$f.txt 2>&1 || echo "FAILED MJ2 $f"
  check; SS3_V=Jsrc SS1_FOOT=$f nice -n 10 python3 ss3_cosmo.py > run_cosmo_Jsrc_$f.txt 2>&1 || echo "FAILED Jsrc $f"
done
echo "[chain] done"
