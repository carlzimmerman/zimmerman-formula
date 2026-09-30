#!/bin/sh
# re-run every script of lane X2; exit 0 iff all exit 0
cd "$(dirname "$0")" || exit 1
rc=0
for f in x01_fluid_perturbations_dS x02_point_mass_in_vacuum x03_what_it_would_take x04_final_table; do
  python3 "$f.py" > "$f.out" 2>&1 || rc=1
  printf '%s: ' "$f"; tail -n 1 "$f.out"
done
exit $rc
