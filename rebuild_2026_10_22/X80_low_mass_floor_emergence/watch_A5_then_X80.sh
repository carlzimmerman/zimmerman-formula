#!/bin/bash
# SUPERSEDED 10-30 by watch_A4_then_X80_then_A5.sh (AMENDMENT_A1.md, owner's decision: X80 before A5). Kept for the record; don't start it.
# Light watcher (one check every 10 min). Waits until X48's A5 watcher logs "A5 done" (so nothing overlaps A4/A5), then
# runs run_low_mass.sh, waits for its 24 done.json, then x80_floor.py and its MUTATE. Log: watch_X80.log. Preempted -> re-run.
cd "$(dirname "$0")"
until grep -q "A5 done" ../X48_native_cf_zoom/watch_A5.log 2>/dev/null; do sleep 600; done
echo "A5 done; launching X80 zooms $(date)"
R=../X48_native_cf_zoom/runs
n=$(ls $R/M1e1[01]_s?_ng{48,64}/done.json 2>/dev/null | wc -l | tr -d ' ')
if [ "$n" -lt 24 ]; then bash run_low_mass.sh; echo "run_low_mass exit $? $(date)"; fi
n=$(ls $R/M1e1[01]_s?_ng{48,64}/done.json 2>/dev/null | wc -l | tr -d ' ')
[ "$n" -lt 24 ] && { echo "X80 incomplete ($n/24 done); not grading $(date)"; exit 75; }
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x80_floor.py > x80_floor.log 2>&1; echo "x80 exit $?"
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x80_floor.py --mutate > x80_floor_MUTATE.log 2>&1; echo "x80 mutate exit $?"
echo "X80 done $(date)"
