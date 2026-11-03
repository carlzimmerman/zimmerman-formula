#!/bin/bash
# BF3 arms in order. Preemptible: rerun resumes. Workers 4.
cd "$(dirname "$0")"
nice -n 19 python3 bf3_search.py real canonical B 4 > arm_real_canonical_B.log 2>&1
nice -n 19 python3 bf3_search.py real canonical A 4 > arm_real_canonical_A.log 2>&1
nice -n 19 python3 bf3_search.py real alt A 4 > arm_real_alt_A.log 2>&1
nice -n 19 python3 bf3_search.py real alt B 4 > arm_real_alt_B.log 2>&1
nice -n 19 python3 bf3_search.py c1 canonical A 4 > arm_c1_A.log 2>&1
nice -n 19 python3 bf3_search.py c1 canonical B 4 > arm_c1_B.log 2>&1
nice -n 19 python3 bf3_search.py c2 canonical A 4 > arm_c2_A.log 2>&1
nice -n 19 python3 bf3_search.py c3 canonical A 4 > arm_c3_A.log 2>&1
BF3_BUDGET_S=7200 nice -n 19 python3 bf3_search.py real canonical E 4 > arm_real_canonical_E.log 2>&1
echo ALLDONE > chain_main.status
