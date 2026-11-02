#!/bin/bash
# Run, rerun to compare, MUTATE twin, clause twin. One thread, nice 19.
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1
nice -n 19 python3 acceptance.py --known > results_known_run.log 2>&1; echo "run $?" > results_known_runs.status
mkdir -p results_known_run_a; cp results/* results_known_run_a/
nice -n 19 python3 acceptance.py --known > results_known_run2.log 2>&1; echo "rerun $?" >> results_known_runs.status
diff -rq results results_known_run_a >> results_known_runs.status; echo "diff done" >> results_known_runs.status
RQ2_MUTATE=1 nice -n 19 python3 acceptance.py --known > results_known_run_mut.log 2>&1; echo "mutate $?" >> results_known_runs.status
RQ3_TWIN=clause nice -n 19 python3 acceptance.py --known > results_known_run_twin.log 2>&1; echo "twin $?" >> results_known_runs.status
echo finished >> results_known_runs.status
