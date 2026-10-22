#!/bin/bash
cd "$(dirname "$0")"
for m in newton_jeans wrong_aperture_radius corrupt_virial shift_anisotropy invert_b_lens tophat_psf deproj_bad beta_sign; do
  A85_MUTATE=$m python3 a85_checks.py > a85_MUTATE_$m.out 2>&1
  echo "$m EXIT $?"
done
