#!/usr/bin/env bash
# CFG264: re-run every script in both modes; exit non-zero on any FAIL.
set -e
cd "$(dirname "$0")"
for s in r1_virial_lambda.py r2_two_sided_junction.py od_horizon_quarter.py; do
  python3 "$s" > /dev/null
  python3 "$s" --mutate > /dev/null
done
python3 cfg264_collect.py
grep -h "^SUMMARY" *.out
