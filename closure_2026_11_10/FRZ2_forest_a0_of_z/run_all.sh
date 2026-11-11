#!/bin/bash
# FRZ2 runner: 24 halo-model jobs (4 at once), then forest per footing and the MZ1 arm. Writes run_all.done.
cd "$(dirname "$0")"; rm -f run_all.done; mkdir -p hm logs
for c in P0 P0.5 P1 P1.5 P2 D-Pan D-DES5 D-Uni Q-Pan Q-DES5 Q-Uni H; do for f in canonical alt; do echo "$c $f"; done; done |
  xargs -P 4 -L 1 bash -c 'FRZ2_CASE=$0 FRZ2_FOOT=$1 nice -n 19 python3 frz2_hm.py > logs/hm_$0_$1.log 2>&1'
for f in canonical alt; do HLF1_FOOT=$f nice -n 19 python3 frz2_forest.py > logs/forest_$f.log 2>&1 &
  HLF1_FOOT=$f HLF1_MUTATE=1 nice -n 19 python3 frz2_forest.py > logs/forest_${f}_MUTATE.log 2>&1 & done; wait
touch run_all.done
