#!/bin/bash
# Light watcher (one check every 10 min). Waits until X74's post-A4 watcher logs "post-A4 regrades done", then launches
# A5 (run_direct_A5.sh), waits for its nine done.json, then runs the A5 analysis, grade and the graded X74 SPARC read
# (criteria a0cbcc6928). Log: watch_A5.log. If A5 is preempted (exit 75), re-run this script; it resumes.
cd "$(dirname "$0")"
until grep -q "post-A4 regrades done" ../X74_all_measured_native_cf/watch_A4.log 2>/dev/null; do sleep 600; done
echo "A4 regrades done; launching A5 $(date)"
n=$(ls runs/M1e12_s?_ng80/done.json 2>/dev/null | wc -l | tr -d ' ')
if [ "$n" -lt 9 ]; then bash run_direct_A5.sh; echo "run_direct_A5 exit $? $(date)"; fi
n=$(ls runs/M1e12_s?_ng80/done.json 2>/dev/null | wc -l | tr -d ' ')
[ "$n" -lt 9 ] && { echo "A5 incomplete ($n/9 done); not grading $(date)"; exit 75; }
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x48_analyze.py --ng 80 --tag A5 > x48_analyze_ng80_A5.out 2>&1; echo "analyze exit $?"
python3 x48_grade_A5.py; echo "grade exit $?"
python3 x48_A5_x74_read.py; echo "X74 read exit $?"
echo "A5 done $(date)"
