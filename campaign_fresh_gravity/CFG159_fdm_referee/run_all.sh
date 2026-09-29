#!/bin/bash
# CFG159 re-run: main + MUTATE A-E of the SP solver, and the G2 check with its control.  Exit codes are recorded in exit_codes.txt.
# Expected: main exits 1 (frozen lines P7a and P8a/P8b fail, kept), every MUTATE exits 1 when it bites.
cd "$(dirname "$0")"
: > exit_codes.txt
python3 CFG159_sp_riccati.py > run_main.console.txt 2>&1; echo "main $?" >> exit_codes.txt
for M in A B C D E; do MUTATE=$M python3 CFG159_sp_riccati.py > run_mut_$M.console.txt 2>&1; echo "MUTATE_$M $?" >> exit_codes.txt; done
python3 CFG159_g2_hbg.py > run_g2.console.txt 2>&1; echo "g2 $?" >> exit_codes.txt
MUTATE=1 python3 CFG159_g2_hbg.py > run_g2_mut.console.txt 2>&1; echo "g2_MUTATE $?" >> exit_codes.txt
echo done >> exit_codes.txt
