#!/bin/bash
# Re-runs every CFG49 script with its MUTATE controls (main runs need MUTATE unset). About 15 minutes (CV6_B and CV6_C dominate).
cd "$(dirname "$0")"
rm -f CV6_B_mu_cache.json
run(){ n=$1; m=$2; if [ -z "$m" ]; then env -u MUTATE python3 $n.py > $n.out 2>&1; echo "rc=$?" >> $n.out; else MUTATE=$m python3 $n.py > ${n}_MUTATE_$m.out 2>&1; echo "rc=$?" >> ${n}_MUTATE_$m.out; fi; }
run CV6_A_local_linear ""; run CV6_A_local_linear a; run CV6_A_local_linear b
run CV6_B_layers ""; run CV6_B_layers a; run CV6_B_layers b
run CV6_C_switched_stiffness ""; run CV6_C_switched_stiffness k
run CV6_D_T3_sensitivity ""; run CV6_D_T3_sensitivity x30
echo ALLDONE > run_all.done
