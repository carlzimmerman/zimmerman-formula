#!/bin/sh
# runs every script of lane L and writes the .out files; exit code = number of failing scripts
cd "$(dirname "$0")"
fail=0
for f in l01_sds_facts l02_principles_E1_E5 l03_pi_count_transcendence l04_conical_quantisation l05_a0point_table_scan_matter; do
  python3 $f.py > $f.out 2>&1 || fail=$((fail+1))
  printf "%s : %s\n" $f "$(tail -1 $f.out)"
done
exit $fail
