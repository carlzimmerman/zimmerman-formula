#!/bin/bash
# XJ1 build A (FROZEN_CRITERIA.md ef8ccdde98, sections 8 and 10): FWN2 build A's runner (run_a.sh in
# closure_2026_11_14/FWN2_forest_flux_split_f4) with this lane's stages. One heavy part at a time, nice 19, 3 flux threads.
# A process exits 76 when its physical footprint passes 14 GB (or peak resident memory 16 GB) and is restarted (it resumes
# from the box files); exit 75 = SIGTERM between boxes. Restartable: finished parts are skipped.
# Mode "all" first WAITS (recheck every 120 s) until FWN2 build A has finished (its run_a.done marker exists).
# Before every part (FWN2 build A's guard, unchanged): STOP (exit 3 / 4) if free disk < 8 GB or swap used > 14 GB; otherwise
# WAIT (recheck every 60 s) until free disk >= 10 GB and free + inactive memory >= 24 GB.
# Usage: run_a.sh tables | test | all
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
cd "$(dirname "$0")"
if [ "$1" = "all" ]; then
  while [ ! -f ../FWN2_forest_flux_split_f4/run_a.done ]; do
    echo "waiting for FWN2 build A to finish (its run_a.done marker) ($(date +%H:%M))"; sleep 120
  done
  echo "FWN2 build A marker present ($(date +%H:%M)); starting"
fi
export XJ1A_THREADS=3 XJ1A_MEM_GB=16 XJ1A_FOOT_GB=14
guard() {
  while true; do
    avail=$(df -g . | awk 'NR==2 {print $4}')
    swap=$(sysctl -n vm.swapusage | sed -E 's/.*used = ([0-9.]+)M.*/\1/')
    pg=$(vm_stat | awk '/page size of/ {print $8}')
    fi_gb=$(vm_stat | awk -v pg="$pg" '/Pages free:/ {f=$3} /Pages inactive:/ {i=$3} END {gsub(/\./,"",f); gsub(/\./,"",i); printf "%d", (f + i) * pg / 1e9}')
    echo "guard: disk ${avail} GB free, swap used ${swap} MB, free+inactive ${fi_gb} GB ($(date +%H:%M))"
    if [ "$avail" -lt 8 ]; then echo "STOP: free disk below 8 GB"; exit 3; fi
    if [ "$(echo "$swap > 14336" | bc)" -eq 1 ]; then echo "STOP: swap used above 14 GB"; exit 4; fi
    if [ "$avail" -ge 10 ] && [ "$fi_gb" -ge 24 ]; then return 0; fi
    echo "  waiting: need free disk >= 10 GB and free+inactive >= 24 GB"; sleep 60
  done
}
part() {
  guard
  while true; do
    nice -n 19 python3 -I -B xj1a_run.py "$@"; rc=$?
    if [ $rc -eq 0 ]; then return 0; elif [ $rc -eq 76 ]; then continue; else echo "stopped rc $rc at $*"; exit $rc; fi
  done
}
guard
[ -f logs/run_a_tables.done ] || { nice -n 19 python3 -I -B xj1a_tables.py 2.2 3.0 4.4 2.6 3.4 3.8 2.4 2.8 3.2 3.6 4.0 4.2 && touch logs/run_a_tables.done; } || exit 2
[ -f xj1a_ka.json ] || nice -n 19 python3 -I -B xj1a_ka.py || exit 6
for f in canonical alt; do [ -f xj1a_c0_$f.json ] || nice -n 19 python3 -I -B xj1a_c0.py $f || exit 5; done
[ "$1" = "tables" ] && exit 0
if [ "$1" = "test" ]; then part e 2.2 0 canonical; exit 0; fi
for s in 0 1 2 3 4 5 6 7 8 9 10 11; do for f in canonical alt; do part e 2.2 $s $f; done; done
for z in 3.0 4.4 2.6 3.4 3.8; do for f in canonical alt; do part oz $z 0 $f; done; done
for f in canonical alt; do part bracketF 2.2 0 $f; done
for f in canonical alt; do part clusteredF 2.2 0 $f; done
for f in canonical alt; do part bracketF 3.0 0 $f; done
touch run_a.done
