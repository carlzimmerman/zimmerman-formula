#!/bin/bash
# XJ1 AMENDMENT_A6: all 12 FLD1 masses x 2 footings, 6 at a time; finished rows are skipped; then the containment script.
cd "$(dirname "$0")"
mkdir -p logs shells45
run() { [ -f shells45/xj1_shells45_$1_M$2.json ] || nice -n 19 python3 -I -B xj1_shells45.py $1 $2 > logs/shells45_$1_$2.log 2>&1; }
for ft in canonical alt; do
  for grp in "6.5 7 8 9 9.4 10" "10.45 10.7 10.9 11.2 11.5 12"; do
    for m in $grp; do run $ft $m & done; wait
  done
done
nice -n 19 python3 -I -B xj1_contain45.py > logs/contain45.log 2>&1
touch logs/shells45.done
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
