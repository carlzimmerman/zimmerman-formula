#!/bin/sh
# runs every script of lane S and rewrites the .out files; exit code = number of failing scripts (a script fails if it exits non-zero or prints any FAIL line)
cd "$(dirname "$0")"
fail=0
for f in s01_brown_york s02_newtonian_action_and_localisation s03_deepmond_field_energy s04_principle_scan s05_the_factor_four; do
  python3 $f.py > $f.out 2>&1 || fail=$((fail+1))
  grep -q "^FAIL" $f.out && fail=$((fail+1))
  printf "%s : %s\n" $f "$(grep '^TOTAL' $f.out | tail -1)"
done
exit $fail
