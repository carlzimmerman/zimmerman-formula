#!/bin/bash
# reproduces every result in README.md (about 1-2 minutes total; sympy + mpmath + numpy only)
cd "$(dirname "$0")"
for f in g01_origin_of_32pi g02_gw_candidates_pi_count g03_graviton_bath_pi_class; do
  python3 -u $f.py > $f.out 2>&1; echo "$f exit=$?  $(tail -1 $f.out)"
done
