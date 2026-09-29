#!/bin/bash
# Re-run everything.  From this directory:  ZF_REPO=<repo root> bash run_all.sh
# (main runs exit 0 unless a reproduction control failed; MUTATE runs exit 1 when the control bites.)
cd "$(dirname "$0")"
: "${ZF_REPO:?set ZF_REPO to the repository root}"
export PYTHONDONTWRITEBYTECODE=1
for s in CFG172_A1_static_reductions CFG172_A2_stability_pincer CFG172_A3_ppn_frame CFG172_A4_growth CFG172_A6_b_operating_point CFG172_A7_c_response CFG172_A5_reaction_energy CFG172_A8_stress_energy; do
  python3 $s.py > $s.out 2>&1; echo "main   $s exit=$?"
done
declare -a MUT=("CFG172_A1_static_reductions:M1" "CFG172_A1_static_reductions:M2" "CFG172_A1_static_reductions:M3" "CFG172_A2_stability_pincer:M2" "CFG172_A2_stability_pincer:M3" \
 "CFG172_A3_ppn_frame:M5" "CFG172_A4_growth:M2" "CFG172_A6_b_operating_point:M1" "CFG172_A6_b_operating_point:M6" "CFG172_A7_c_response:M3" "CFG172_A7_c_response:M4" \
 "CFG172_A8_stress_energy:M7" "CFG172_A8_stress_energy:M8")
for m in "${MUT[@]}"; do
  s=${m%%:*}; k=${m##*:}
  MUTATE=$k python3 $s.py > ${s}_MUTATE_$k.out 2>&1; echo "MUTATE $s $k exit=$? (1 = the control bites)"
done
python3 CFG172_verdict.py > CFG172_verdict.out 2>&1; echo "verdict exit=$?"
