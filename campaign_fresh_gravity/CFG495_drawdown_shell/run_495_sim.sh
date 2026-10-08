#!/bin/bash
# CFG495 Step 1 launcher: one 512^3-size job in memory at a time, nice 15, 4 threads.
cd "$(dirname "$0")"
W=../../../_external_data/cfg495_work
for k in N512_s360_can N512_s359_alt N512_s359_can N256_s359_alt; do
  nice -n 15 python3 cfg495_sim.py $k > $W/log_$k.txt 2>&1; echo "$k rc $?" >> $W/launcher.log
done
for k in N512_s360_can N256_s359_can; do
  CFG495_MUTATE=1 nice -n 15 python3 cfg495_sim.py $k > $W/log_${k}_MUTATE.txt 2>&1; echo "$k MUTATE rc $?" >> $W/launcher.log
done
