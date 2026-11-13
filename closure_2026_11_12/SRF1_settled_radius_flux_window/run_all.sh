#!/bin/bash
# SRF1: one job, stages in order (AMENDMENT_A1 item 7). nice 19, 2 flux threads. One box per python process (base box, then
# each forced group, then merge): macOS does not return freed memory inside a process. Restartable; stops on the first failure.
cd "$(dirname "$0")"
export SRF1_THREADS=2
set -e
part() {
  nice -n 19 python3 srf1_run.py one "$@" base
  for g in $(python3 srf1_run.py groups "$@"); do nice -n 19 python3 srf1_run.py one "$@" "$g"; done
  nice -n 19 python3 srf1_run.py one "$@" merge
}
for z in 2.2 3.0 4.4; do for s in 0 1; do for f in canonical alt; do part primary $z $s $f; done; done; done
for z in 2.4 2.6 2.8 3.2 3.4 3.6 3.8 4.0 4.2; do for f in canonical alt; do part primary $z 0 $f; done; done
for z in 2.2 3.0; do for f in canonical alt; do part bracket $z 0 $f; done; done
for f in canonical alt; do part clustered 2.2 0 $f; done
for f in canonical alt; do part res 2.2 0 $f; done
touch run_all.done
