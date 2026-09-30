#!/bin/bash
# Lane Z1: reruns everything (about 40 s).  Exit 0 iff every script passes all its checks.
cd "$(dirname "$0")"
fail=0
for s in z01_cutoff_laws z02_data_constraints z03_milgrom_table z04_kurvs_pipeline z05_decisive_tests z06_coincidence_Rstar_Rp; do
  python3 $s.py > $s.out 2>&1 || { echo "FAIL $s"; fail=1; }
  echo "$s: $(tail -1 $s.out)"
done
for m in 1 2; do
  MUTATE=$m python3 z04_kurvs_pipeline.py > z04_kurvs_pipeline_MUTATE$m.out 2>&1 || { echo "FAIL z04 MUTATE=$m"; fail=1; }
  echo "z04 MUTATE=$m: $(tail -1 z04_kurvs_pipeline_MUTATE$m.out)"
done
exit $fail
