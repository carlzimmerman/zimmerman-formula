#!/usr/bin/env bash
# CFG231 -- run everything: seven analysis scripts (main), the verdict table, and the MUTATE controls MU1-MU8.
# Exit convention: a main script exits 0 iff its reproduction controls pass; a MUTATE run exits 1 iff the control BITES
# (the named headline differs from the main run's); MU5 is a declared non-biting control (exit 0, kept).
# Repo root: ZF_REPO if set, else found by walking up from this file. No absolute path is printed.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE" || exit 2
export PYTHONDONTWRITEBYTECODE=1
fail=0
for s in A1_point_mass_algebra A2_sphere_charge_function A3_vector_class A4_cosmology A5_reaction_energy A6_solar_stability A7_normalisation_ledger verdict; do
  python3 "CFG231_${s}.py" > /dev/null 2>"CFG231_${s}.stderr"
  rc=$?
  [ -s "CFG231_${s}.stderr" ] || rm -f "CFG231_${s}.stderr"
  echo "main   CFG231_${s}: exit ${rc}"
  [ "$rc" -eq 0 ] || fail=1
done
# MUTATE runs: script:mode:expected_exit (1 = bites)
for sm in A2_sphere_charge_function:MU1:1 A2_sphere_charge_function:MU4:1 A2_sphere_charge_function:MU5:0 A2_sphere_charge_function:MU8:1 \
          A6_solar_stability:MU2:1 A6_solar_stability:MU3:1 A6_solar_stability:MU6:1 A6_solar_stability:MU7:1 \
          A7_normalisation_ledger:MU2:1 A7_normalisation_ledger:MU4:1; do
  IFS=: read -r s m want <<< "$sm"
  MUTATE="$m" python3 "CFG231_${s}.py" > /dev/null 2>&1
  rc=$?
  tag="as expected"; [ "$rc" -eq "$want" ] || { tag="UNEXPECTED"; fail=1; }
  echo "MUTATE CFG231_${s} ${m}: exit ${rc} (expected ${want}; ${tag})"
done
echo "overall: $([ $fail -eq 0 ] && echo OK || echo SOMETHING UNEXPECTED)"
exit $fail
