#!/bin/bash
# BF3 arms under Amendment A2. Preemptible: rerun resumes.
cd "$(dirname "$0")"
run() { b=$1; shift; BF3_BUDGET_S=$b nice -n 19 python3 bf3_search.py "$@" 4 > "arm_$1_$2_$3.log" 2>&1; }
run 7200 real canonical A
run 2400 r10 canonical A
run 2400 c1 canonical A
run 2400 c2 canonical A
run 2400 c3 canonical A
run 2400 real alt A
run 2400 real alt B
run 2400 c1 canonical B
run 3600 real canonical E
echo ALLDONE > chain2.status
