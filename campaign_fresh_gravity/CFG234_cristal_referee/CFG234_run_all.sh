#!/bin/bash
# CFG234: run everything in the frozen order. ZF_REPO=<repo> if the repo is not found automatically (from the scratch dir: python3 finds ~/new_physics/zimmerman-formula).
cd "$(dirname "$0")" || exit 1
{
python3 CFG234_main.py > /dev/null;                 echo "main exit $? (0 = C1, C2, C4-vs-CFG5, M7 recovery pass)"
for k in 1 2 3 4 5 6 7; do MUTATE=$k python3 CFG234_MUTATE.py > /dev/null; echo "MUTATE $k exit $? (1 = the control bites)"; done
python3 CFG234_attack_b.py > /dev/null;             echo "attack b exit $?"
python3 CFG234_attack_c.py > /dev/null;             echo "attack c exit $?"
python3 CFG234_attack_d.py > /dev/null;             echo "attack d exit $?"
SEED=234 python3 CFG234_attack_e.py > /dev/null;    echo "attack e seed 234 exit $?"
SEED=235 python3 CFG234_attack_e.py > /dev/null;    echo "attack e seed 235 exit $?"
python3 CFG234_attack_f.py > /dev/null;             echo "attack f exit $?"
python3 CFG234_postfreeze.py > /dev/null;          echo "postfreeze exit $? (post-freeze item, labelled)"
python3 CFG234_compare.py > /dev/null;              echo "compare exit $? (post-comparison with CFG213's committed results; opens CFG213's JSON, so run it only after the referee runs above)"
} 2>&1 | tee run_all.out
