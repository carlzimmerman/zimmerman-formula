#!/usr/bin/env bash
#
# run_all.sh  --  Execute the full 12-gate closure attack and aggregate results.
#
# Usage:   bash run_all.sh
#
# Each gate script prints a line of the form  "GATE <n> RESULT: PASS|FAIL"
# (the merged script 04 prints GATE 4/5/6 RESULT lines).  This harness runs
# every script, collects the PASS/FAIL verdicts, and prints a final summary.
# Exit code is 0 iff every gate PASSes.
#
# (Compatible with bash 3.2: no associative arrays.)

set -u
cd "$(dirname "$0")/scripts"

PY="${PYTHON:-python3}"

SCRIPTS="01_constitutive.py 02_newtonian_limit.py 03_dirac_matrix.py \
04_rank_and_ellipticity.py 05_dof_count.py 06_constraint_preservation.py \
07_tensor_sector.py 08_matter_consistency.py 09_legendre_check.py \
12_falsification.py"

overall=0
summary=""

echo "############################################################################"
echo "#  MOND MMG 2-DOF HAMILTONIAN CLOSURE  --  12-GATE ATTACK                #"
echo "############################################################################"

for s in $SCRIPTS; do
    echo
    echo "############################################################################"
    echo "#  RUNNING  $s"
    echo "############################################################################"
    out="$("$PY" "$s" 2>&1)"
    status=$?
    echo "$out"

    if echo "$out" | grep -q "RESULT: FAIL"; then
        verdict="FAIL"
        overall=1
    elif echo "$out" | grep -q "RESULT: PASS"; then
        verdict="PASS"
    else
        verdict="NO-VERDICT (exit $status)"
        overall=1
    fi
    summary="${summary}  ${s} : ${verdict}"$'\n'
done

echo
echo "############################################################################"
echo "#  SUMMARY"
echo "############################################################################"
printf "%s" "$summary"
echo "############################################################################"
if [ "$overall" -eq 0 ]; then
    echo "  ALL GATES PASS"
else
    echo "  SOME GATES FAILED / NO VERDICT"
fi
echo "############################################################################"
exit "$overall"
