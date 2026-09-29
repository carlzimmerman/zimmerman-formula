#!/bin/bash
# Re-run CFG121 in place.  Needs ZF_REPO (repo root) unless this directory sits inside the repo.  Order matters: B before C, E, S (P_star).
# Main runs exit 0; MUTATE runs exit 1 when the declared cell changed (0 = control failed, reported).
cd "$(dirname "$0")"
python3 T1_required_chi_and_local_law.py > /dev/null; echo "T1 main rc $?"
python3 B_budget_pincer.py > /dev/null; echo "B main rc $?"
python3 C_cosmology_growth.py > /dev/null; echo "C main rc $?"
python3 E_reaction_energy_noether.py > /dev/null; echo "E main rc $?"
python3 S_stability_solar_ownership.py > /dev/null; echo "S main rc $?"
for m in sign kernel; do MUTATE=$m python3 T1_required_chi_and_local_law.py > /dev/null; echo "T1 MUTATE=$m rc $?"; done
MUTATE=Q10 python3 B_budget_pincer.py > /dev/null; echo "B MUTATE=Q10 rc $?"
MUTATE=Q10 python3 C_cosmology_growth.py > /dev/null; echo "C MUTATE=Q10 rc $?"
MUTATE=recip python3 E_reaction_energy_noether.py > /dev/null; echo "E MUTATE=recip rc $?"
for m in kernel nofield; do MUTATE=$m python3 S_stability_solar_ownership.py > /dev/null; echo "S MUTATE=$m rc $?"; done
# second a0 footing (1.1312e-10): FOOTING=second python3 <script>  (B first)
# post-hoc (not frozen): python3 posthoc_G2_pincer.py
