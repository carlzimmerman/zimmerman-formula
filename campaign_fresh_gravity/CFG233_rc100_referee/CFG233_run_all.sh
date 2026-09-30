#!/bin/bash
# Re-run command (from the scratch dir, or with CFG233 scripts anywhere): bash CFG233_run_all.sh   [ZF_REPO=<repo> if not found automatically]
# Runs every frozen script on BOTH tables: DATA=committed (the csv CFG216 used) and DATA=corrected (six-field paper values, disclosed alongside).
cd "$(dirname "$0")"
for DATA in committed corrected; do
  export DATA
  echo "=== DATA=$DATA" 
  python3 CFG233_main.py > /dev/null 2>&1; echo "main exit $?"
  for k in 1 2 3 4 5 6 7; do MUTATE=$k python3 CFG233_MUTATE.py > /dev/null 2>&1; echo "MUTATE $k exit $? (1 = bites)"; done
  python3 CFG233_attack_a.py > /dev/null 2>&1; echo "attack a exit $?"
  SEED=233 python3 CFG233_attack_b.py > /dev/null 2>&1; echo "attack b seed 233 exit $?"
  SEED=234 python3 CFG233_attack_b.py > /dev/null 2>&1; echo "attack b seed 234 exit $?"
  python3 CFG233_attack_c.py > /dev/null 2>&1; echo "attack c exit $?"
  python3 CFG233_attack_d.py > /dev/null 2>&1; echo "attack d exit $?"
  python3 CFG233_attack_e.py > /dev/null 2>&1; echo "attack e exit $?"
done
DATA=committed python3 CFG233_rows_changed.py > /dev/null 2>&1; echo "rows_changed exit $?"
python3 CFG233_compare.py > /dev/null 2>&1; echo "compare exit $?"
