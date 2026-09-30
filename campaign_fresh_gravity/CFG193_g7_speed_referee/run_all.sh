#!/bin/bash
# CFG193 re-run. From this directory: ZF_REPO=<repo root> bash run_all.sh   (about an hour on a loaded machine; outputs are written next to the scripts)
# Expected exit codes: mains 0; MUTATE 1-4 and 6 of the c script exit 1 (bite); MUTATE 5 exits 3 (kernel-robust, does not bite).
cd "$(dirname "$0")" || exit 2
: "${ZF_REPO:?set ZF_REPO to the repository root}"
export ZF_REPO PYTHONDONTWRITEBYTECODE=1
python3 CFG193_a_velocities.py > /dev/null; echo "a rc=$?"
python3 CFG193_b_curves.py > /dev/null; echo "b rc=$?"
for k in 1 3 5; do MUTATE=$k python3 CFG193_b_curves.py > /dev/null; echo "b MUTATE=$k rc=$?"; done
python3 CFG193_c_fit_power.py > /dev/null; echo "c rc=$?"
for k in 1 2 3 4 5 6; do MUTATE=$k python3 CFG193_c_fit_power.py > /dev/null; echo "c MUTATE=$k rc=$?"; done
python3 CFG193_d_design.py > /dev/null; echo "d rc=$?"
python3 CFG193_e_profile.py > /dev/null; echo "e rc=$?"
for s in b_curves c_fit_power e_profile; do CFG193_VARIANT=U2 python3 CFG193_$s.py > /dev/null; echo "$s U2 rc=$?"; done
python3 CFG193_compare.py > /dev/null; echo "compare rc=$? (opens CFG186's files)"
