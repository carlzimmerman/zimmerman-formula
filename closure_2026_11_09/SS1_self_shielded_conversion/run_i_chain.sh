#!/bin/bash
# SS1 variant I chain (AMENDMENT_A5): one child at a time, nice 10, df check (stop under 2 GiB free).
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1
check() { free=$(df -g . | tail -1 | awk '{print $4}'); echo "[chain] df free ${free} GiB before $1"; if [ "$free" -lt 2 ]; then echo "[chain] STOP"; exit 3; fi; }
r() { tag=$1; shift; check $tag; nice -n 10 python3 ss1v.py "$@" > run_i_$tag.txt 2>&1 || echo "[chain] FAILED $tag"; }
for V in I Isrc Inob; do r local_$V local $V; for f in canonical alt; do SS1_FOOT=$f r cosmo_${V}_$f cosmo $V; done; r bullet_$V bullet $V; done
for V in MI1 MI2; do r local_$V local $V; for f in canonical alt; do SS1_FOOT=$f r cosmo_${V}_$f cosmo $V; done; done
echo "[chain] done"
