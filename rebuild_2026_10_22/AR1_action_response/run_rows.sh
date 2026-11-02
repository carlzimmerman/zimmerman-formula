#!/bin/bash
# AR1 graded rows, grid (192, 32, 64, dl 0.005). One thread each, nice 15. SIGTERM -> checkpoint; rerun resumes. Prints no graded number.
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
nice -n 15 python3 ar1_sparc.py hand_act_inv hand_act_inv_t2 >> s1.log 2>&1 &
nice -n 15 python3 ar1_sparc.py hand_act_v2r nat_act_inv >> s2.log 2>&1 &
nice -n 15 python3 ar1_sparc.py hand_act_exp nat_act_v2r >> s3.log 2>&1 &
nice -n 15 python3 ar1_sparc.py hand_act_inv_mut2 >> s4.log 2>&1 &
nice -n 15 python3 ar1_clusters.py erass >> c1.log 2>&1 &
nice -n 15 python3 ar1_clusters.py gs5 >> c2.log 2>&1 &
trap 'kill -TERM $(jobs -p) 2>/dev/null; wait; exit 75' TERM INT; wait; echo "AR1 rows done"
