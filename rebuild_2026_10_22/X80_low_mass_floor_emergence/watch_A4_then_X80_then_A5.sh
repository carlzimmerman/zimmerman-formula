#!/bin/bash
# Owner's decision 10-30 (AMENDMENT_A1.md): X80 runs before A5. Light watcher (one check every 10 min). Waits until X74's post-A4 watcher logs
# "post-A4 regrades done", runs the X80 zooms, x80_floor.py and its MUTATE, then the amendment's converged-eta reading and native read, logs
# "X80 done", then hands over to X48's A5 watcher, unchanged. Log: watch_X80.log. Preempted (exit 75) -> re-run this script: it resumes, and A5 doesn't start.
cd "$(dirname "$0")"
until grep -q "post-A4 regrades done" ../X74_all_measured_native_cf/watch_A4.log 2>/dev/null; do sleep 600; done
echo "A4 regrades done; launching X80 zooms $(date)"
R=../X48_native_cf_zoom/runs
n=$(ls $R/M1e1[01]_s?_ng{48,64}/done.json 2>/dev/null | wc -l | tr -d ' ')
if [ "$n" -lt 24 ]; then bash run_low_mass.sh; echo "run_low_mass exit $? $(date)"; fi
n=$(ls $R/M1e1[01]_s?_ng{48,64}/done.json 2>/dev/null | wc -l | tr -d ' ')
[ "$n" -lt 24 ] && { echo "X80 incomplete ($n/24 done); not grading, A5 not started $(date)"; exit 75; }
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x80_floor.py > x80_floor.log 2>&1; echo "x80 exit $?"
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x80_floor.py --mutate > x80_floor_MUTATE.log 2>&1; echo "x80 mutate exit $?"
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x80_converged.py > x80_converged.log 2>&1; echo "x80 converged exit $?"
(cd ../NF1_no_floor_rule && PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 nf1_native_read.py > nf1_native_read.log 2>&1); echo "nf1 native read exit $?"
echo "X80 done $(date)"
cd ../X48_native_cf_zoom && exec bash watch_A4_then_A5.sh >> watch_A5.log 2>&1
