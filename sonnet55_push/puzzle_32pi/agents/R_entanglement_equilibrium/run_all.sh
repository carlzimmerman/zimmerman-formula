#!/bin/bash
# reruns every script of lane R; exit 0 only if all pass
cd "$(dirname "$0")" || exit 1
rc=0
for f in r01_ball_geometry r02_modular_energy_and_chain r03_exact_finite_ball r04_scale_candidates r05_newtonian_and_nonlinear; do
  python3 $f.py > $f.out 2>&1; e=$?
  echo "$f exit $e : $(tail -1 $f.out)"
  [ $e -ne 0 ] && rc=1
done
exit $rc
