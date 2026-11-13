#!/bin/bash
# FRZ4: one job, stages in the frozen order (FROZEN_CRITERIA.md section 4). nice 19, 2 flux threads. A process exits 76 when its
# peak memory passes 12 GB and is restarted (it resumes from the box files); exit 75 = SIGTERM between boxes. Restartable.
cd "$(dirname "$0")"
export FRZ4_THREADS=2
part() {
  while true; do
    nice -n 19 python3 frz4_run.py "$@"; rc=$?
    if [ $rc -eq 0 ]; then return 0; elif [ $rc -eq 76 ]; then continue; else echo "stopped rc $rc at $*"; exit $rc; fi
  done
}
[ -f logs/tables.done ] || nice -n 19 python3 frz4_tables.py 2.2 3.0 4.4 2.6 3.4 3.8 2.4 2.8 3.2 3.6 4.0 4.2
for z in 2.2 3.0 4.4 2.6 3.4 3.8; do for f in canonical alt; do part primary $z 0 $f; done; done
for f in canonical alt; do part primary 2.2 1 $f; done
for f in canonical alt; do part bracket 2.2 0 $f; done
for f in canonical alt; do part clustered 2.2 0 $f; done
for f in canonical alt; do part bracket 3.0 0 $f; done
touch run_all.done
