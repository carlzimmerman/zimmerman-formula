#!/bin/sh
# re-run every script of lane M and print the pass counts (each script exits 0 only if all its checks pass)
cd "$(dirname "$0")"
for s in m01_kinematical_jacobi m02_dilatation_weights m03_conformal_galilei_ladder m04_cohomology m05_equivariant_deformations m06_a0_direction_and_H_spectrum m07_map_to_acceleration; do
  python3 $s.py > $s.out 2>&1; rc=$?
  echo "$s : exit $rc : $(grep -c '^PASS' $s.out) PASS, $(grep -c '^FAIL' $s.out) FAIL"
done
