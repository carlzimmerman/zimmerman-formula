#!/bin/bash
# JNT2 G1 chain: halo model then forest gate for every mode, one process at a time. Paths relative to this folder.
cd "$(dirname "$0")"
for m in main 0 H D; do
  python3 jnt2_hm.py --mode $m > run_hm_$m.log 2>&1; echo "exit $?" >> run_hm_$m.log
done
for m in main S 0 H D; do
  for f in canonical alt; do JNT2_FOOT=$f python3 jnt2_forest.py --mode $m > run_forest_${f}_$m.log 2>&1; echo "exit $?" >> run_forest_${f}_$m.log; done
done
touch done_g1
