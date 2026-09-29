#!/bin/bash
cd "$(dirname "$0")"
for s in T1_required_chi_and_local_law B_budget_pincer C_cosmology_growth E_reaction_energy_noether S_stability_solar_ownership; do FOOTING=second python3 $s.py > /dev/null; echo "$s second rc $?"; done
python3 posthoc_G2_pincer.py > /dev/null; echo "posthoc G2 rc $?"
python3 posthoc_C2_by_amplitude.py > /dev/null; echo "posthoc C2 rc $?"
