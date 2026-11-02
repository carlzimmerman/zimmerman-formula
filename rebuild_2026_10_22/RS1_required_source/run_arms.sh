#!/bin/bash
# RS1 Part 2, two at a time at most. Rerun resumes.
cd "$(dirname "$0")"; export PYTHONHASHSEED=0 OMP_NUM_THREADS=1; P="nice -n 10 python3 -I rs1_search.py"
( $P canonical U50 real; $P alt U50 real; $P canonical U50 shuf ) > runs/lane1.log 2>&1 &
( $P canonical low real; $P alt low real ) > runs/lane2.log 2>&1 &
wait; echo ALLDONE > runs/all.done
