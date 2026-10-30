#!/bin/bash
# CE1 post-A4 rerun: waits for X77's A4 rerun (A4_x77_results.json, written by X77's run_after_A4.sh after all 18 A4
# snapshots), then waits for X77's A4 grades to finish, then runs ce1_grade.py --A4 (outputs CE1_A4_*). Nothing committed.
cd "$(dirname "$0")"
X77=../X77_direct_core_surface_density
while [ ! -f $X77/A4_x77_results.json ] || ! grep -q "X77 A4 rerun done" $X77/A4_watch.log 2>/dev/null; do sleep 900; done
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ce1_grade.py --A4 > ce1_A4_run.log 2>&1
echo "CE1 A4 done $(date)" >> watch_A4_CE1.log
