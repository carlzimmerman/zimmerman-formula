#!/bin/bash
# BK2 driver: nice 19, one thread, one per footing. Resumes: rerun after a stop. python3 from PATH. Harvest after each run.
cd "$(dirname "$0")"; FOOT=$1; export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
for job in "planted L1" "real L1" "mutate L1" "control L1" "real L2" "control L2"; do set -- $job
  [ "$1" = planted ] && [ "$FOOT" = alt ] && continue
  W=chunks/$2_${FOOT}_$1; [ -f "$W/COMPLETE" ] || nice -n 19 python3 bk2_search.py $FOOT $1 $2 >> bk2_${FOOT}_$1_$2.log 2>&1 || exit 1
  [ -f "$W/COMPLETE" ] || exit 2
  [ -f "$W/READ" ] || { nice -n 19 python3 bk2_read.py $FOOT $1 $2 > bk2_read_$2_${FOOT}_$1.out 2>&1 && touch "$W/READ"; }
done; echo finished > chunks/driver_${FOOT}.done
