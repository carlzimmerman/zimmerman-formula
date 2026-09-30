#!/bin/sh
# re-run every script of lane N; exit 0 iff all exit 0
cd "$(dirname "$0")" || exit 1
rc=0
for f in n01_dS_unruh_structure n02_jacobson_chain n03_dS_clausius_no_crossover n04_conversion_and_crossover; do
  python3 "$f.py" > "$f.out" 2>&1 || rc=1
  printf '%s: ' "$f"; tail -n 1 "$f.out"
done
exit $rc
