#!/usr/bin/env bash
# CFG188 re-run.  Usage (from the directory holding these scripts):  ZF_REPO=<repo root> bash run_all.sh
# Main runs exit 0 iff their reproduction controls pass; MUTATE runs exit 1 when the control bites.
cd "$(dirname "$0")" || exit 2
: "${ZF_REPO:?set ZF_REPO to the repository root}"
export ZF_REPO
for s in R1_static_reduction R2_stability_tail R3_b_operating_point R4_c_response; do
  python3 CFG188_$s.py > CFG188_$s.out 2>&1; echo "CFG188_$s main exit=$?"
done
for pair in R1_static_reduction:M3 R1_static_reduction:M4 R1_static_reduction:M9 R2_stability_tail:M1 R2_stability_tail:M2 R2_stability_tail:M10 R3_b_operating_point:M5 R3_b_operating_point:M6 R4_c_response:M7 R4_c_response:M8; do
  s=${pair%%:*}; m=${pair##*:}
  MUTATE=$m python3 CFG188_$s.py > CFG188_${s}_MUTATE_$m.out 2>&1; echo "CFG188_$s MUTATE=$m exit=$? (1 = the control bites)"
done
python3 CFG188_verdict.py > CFG188_verdict.out 2>&1; echo "CFG188_verdict exit=$?"
# departure (added after reading CFG172 A3): pulsar-row acceleration sensitivity of the dressed G6(b) verdict
python3 CFG188_R3b_pulsar_sensitivity.py > CFG188_R3b_pulsar_sensitivity.out 2>&1; echo "CFG188_R3b exit=$?"
