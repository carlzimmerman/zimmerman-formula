#!/bin/bash
# SS2 chain: one child at a time, nice 10, df check (stop under 2 GiB free). SS1_PJ1_DIR: read-only copy of origin's PJ1 lane dir.
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1
check() { free=$(df -g . | tail -1 | awk '{print $4}'); echo "[chain] df free ${free} GiB before $1"; if [ "$free" -lt 2 ]; then echo "[chain] STOP"; exit 3; fi; }
r() { tag=$1; shift; check $tag; nice -n 10 python3 ss2.py "$@" > run_$tag.txt 2>&1 || echo "[chain] FAILED $tag"; }
r ka ka
for f in canonical alt; do SS1_FOOT=$f r valid_$f valid; done
for V in G Gsrc; do r local_$V local $V; for f in canonical alt; do SS1_FOOT=$f r cosmo_${V}_$f cosmo $V; done; r bullet_$V bullet $V; done
r local_G_obs local G obs; r local_G_local local G local
for f in canonical alt; do SS1V_MMIN=1e10 SS1_FOOT=$f r cosmo_G_${f}_mmin1e10 cosmo G; done
for V in MG1 MG2 MG3 MG4; do r local_$V local $V; for f in canonical alt; do SS1_FOOT=$f r cosmo_${V}_$f cosmo $V; done; done
for f in canonical alt; do SS1_FOOT=$f r cosmo_Gz2_$f cosmo Gz2; done
r predict predict
echo "[chain] done"
