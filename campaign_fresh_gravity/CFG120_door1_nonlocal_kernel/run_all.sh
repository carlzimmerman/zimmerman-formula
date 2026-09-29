#!/bin/bash
# CFG120 re-run in place.  Set ZF_REPO to the repository root if these scripts are not inside it (default: the recorded location).
# Main runs (A must come first: it writes the RM best-fit caches cfg120_rmfit_<footing>.json that B, C and D read).
# Exit codes: main runs may exit 1 by design (kept failed pre-declared checks; see the .out files); each MUTATE run below must exit 1.
cd "$(dirname "$0")"
export PYTHONWARNINGS=ignore
python3 cfg120_A_linearity_theorem.py > /dev/null; echo "A main rc=$?"
python3 cfg120_B_mass_functional_kernel.py > /dev/null; echo "B main rc=$?"      # ~8 min (12 processes)
python3 cfg120_C_cosmology_g2.py > /dev/null; echo "C main rc=$?"                # ~5 min
python3 cfg120_D_g3_g4_g5.py > /dev/null; echo "D main rc=$?"                    # ~3 min
python3 cfg120_POSTHOC_diagnostics.py > /dev/null; echo "POSTHOC rc=$?"          # post-hoc, not frozen
# MUTATE controls (bite matrix: a,b -> A;  d -> B, D;  c -> C).  Modes with no bite in a script are declared in that script's header and not run.
MUTATE=a python3 cfg120_A_linearity_theorem.py > /dev/null; echo "A MUTATE=a rc=$? (must be 1)"
MUTATE=b python3 cfg120_A_linearity_theorem.py > /dev/null; echo "A MUTATE=b rc=$? (must be 1)"
MUTATE=d python3 cfg120_B_mass_functional_kernel.py > /dev/null; echo "B MUTATE=d rc=$? (must be 1)"
MUTATE=c python3 cfg120_C_cosmology_g2.py > /dev/null; echo "C MUTATE=c rc=$? (must be 1)"
MUTATE=d python3 cfg120_D_g3_g4_g5.py > /dev/null; echo "D MUTATE=d rc=$? (must be 1)"
