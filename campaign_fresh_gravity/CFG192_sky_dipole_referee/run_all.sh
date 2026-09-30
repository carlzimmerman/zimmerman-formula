#!/bin/bash
# CFG192 run_all: profiles, main, MUTATE 1-7, attacks, (compare = phase 2).  Usage: ZF_REPO=<path to repo> bash run_all.sh
# Exit codes: main 0; MUTATE k exits 1 when the control BITES (0 when it does not; both are recorded); attacks 0.
# A second in-place run must give byte-identical .out files: sha256 of every .out is written to CFG192_SHA256.txt (timings go to stderr only).
set -u
cd "$(dirname "$0")"
: "${ZF_REPO:?set ZF_REPO to the repository root}"
export ZF_REPO
python3 CFG192_profiles.py > /dev/null 2>&1; echo "profiles rc=$?"
for k in 1 2 4 6; do MUTATE=$k python3 CFG192_profiles.py > /dev/null 2>&1; echo "profiles MUTATE=$k rc=$?"; done
python3 CFG192_main.py > /dev/null 2>&1; echo "main rc=$?"
for k in 1 2 3 4 5 6 7; do MUTATE=$k python3 CFG192_main.py > /dev/null 2>&1; echo "main MUTATE=$k rc=$? (1 = control bites)"; done
python3 CFG192_attacks_AB.py > /dev/null 2>&1; echo "attacks_AB rc=$?"
python3 CFG192_attacks_CD.py > /dev/null 2>&1; echo "attacks_CD rc=$?"
python3 CFG192_attacks_E.py > /dev/null 2>&1; echo "attacks_E rc=$?"
if [ -f CFG192_compare.py ]; then python3 CFG192_compare.py > /dev/null 2>&1; echo "compare rc=$?"; fi
sha256sum CFG192_*.out > CFG192_SHA256.txt
echo "wrote CFG192_SHA256.txt"
