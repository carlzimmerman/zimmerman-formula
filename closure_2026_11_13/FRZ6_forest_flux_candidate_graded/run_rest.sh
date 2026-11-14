#!/bin/bash
# FRZ6 resume after the 18:45 stop (spec_list bug): remaining stages only, frozen order. One job, stages in the frozen order (FROZEN_CRITERIA.md section 10). nice 19, 2 flux threads. A process exits 76 when
# its peak memory passes 16 GB and is restarted (it resumes from the box files); exit 75 = SIGTERM between boxes. Restartable.
# Before every part: free disk >= 8 GB and swap used <= 8 GB, else stop (exit 3 / 4).
cd "$(dirname "$0")"
[ -f logs/tables.done ] || exit 2
export FRZ6_THREADS=2 FRZ6_MEM_GB=16
guard() {
  avail=$(df -g . | awk 'NR==2 {print $4}')
  swap=$(sysctl -n vm.swapusage | sed -E 's/.*used = ([0-9.]+)M.*/\1/')
  echo "guard: disk ${avail} GB free, swap used ${swap} MB ($(date +%H:%M))"
  if [ "$avail" -lt 8 ]; then echo "STOP: free disk below 8 GB"; exit 3; fi
  if [ "$(echo "$swap > 8192" | bc)" -eq 1 ]; then echo "STOP: swap used above 8 GB"; exit 4; fi
}
part() {
  guard
  while true; do
    nice -n 19 python3 -I -B frz6_run.py "$@"; rc=$?
    if [ $rc -eq 0 ]; then return 0; elif [ $rc -eq 76 ]; then continue; else echo "stopped rc $rc at $*"; exit $rc; fi
  done
}
guard
for f in canonical alt; do part bracketS 2.2 0 $f; done
for f in canonical alt; do part clusteredS 2.2 0 $f; done
for f in canonical alt; do part bracketS 3.0 0 $f; done
for z in 2.2 3.0; do for f in canonical alt; do part mrU $z 0 $f; done; done
touch run_all.done
