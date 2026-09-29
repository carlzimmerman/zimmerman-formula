#!/bin/bash
# CFG172D re-run. From this directory: ZF_REPO=<repo root> bash run_all.sh   (about 15 min; A3 before A2 and A4, which read A3's zeta_min_reference).
# Main runs exit 0 unless a reproduction control failed; MUTATE runs exit 1 when the control bites (M4 in A4 and M5 in A3 do not bite, kept).
cd "$(dirname "$0")" || exit 2
: "${ZF_REPO:?set ZF_REPO to the repository root}"
export ZF_REPO PYTHONDONTWRITEBYTECODE=1
for s in A1_theta_equation A3_obstruction A2_static_solve A4_gates_G2_G5_G6_G7 A5_stress_energy; do
  python3 CFG172D_$s.py > CFG172D_$s.out 2>&1; echo "main $s exit=$?"
done
python3 CFG172D_verdict.py > CFG172D_verdict.out 2>&1; echo "verdict exit=$?"
for pair in A1_theta_equation:M6 A1_theta_equation:M7 A3_obstruction:M1 A3_obstruction:M2 A3_obstruction:M3 A3_obstruction:M4 A3_obstruction:M5 A2_static_solve:M2 A2_static_solve:M3 A4_gates_G2_G5_G6_G7:M4 A5_stress_energy:M8; do
  s=${pair%%:*}; m=${pair##*:}
  MUTATE=$m python3 CFG172D_$s.py > CFG172D_${s}_MUTATE_$m.out 2>&1; echo "MUTATE $s $m exit=$?"
done
