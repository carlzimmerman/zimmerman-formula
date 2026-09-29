#!/bin/bash
# Re-runs every CFG49 script with its MUTATE controls (main runs need MUTATE unset). About 15 minutes (CV6_B and CV6_C dominate).
cd "$(dirname "$0")"
rm -f CV6_B_mu_cache.json
run(){ n=$1; m=$2; if [ -z "$m" ]; then env -u MUTATE python3 $n.py > $n.out 2>&1; echo "rc=$?" >> $n.out; else MUTATE=$m python3 $n.py > ${n}_MUTATE_$m.out 2>&1; echo "rc=$?" >> ${n}_MUTATE_$m.out; fi; }
run CV6_A_local_linear ""; run CV6_A_local_linear a; run CV6_A_local_linear b
run CV6_B_layers ""; run CV6_B_layers a; run CV6_B_layers b
run CV6_C_switched_stiffness ""; run CV6_C_switched_stiffness k
run CV6_D_T3_sensitivity ""; run CV6_D_T3_sensitivity x30
# Write run_all.done ONLY if every run finished with its expected exit code (mains: 0 except CV6_B, whose declared H2 was refuted, rc 1; every MUTATE: 1);
# otherwise write run_all.failed listing the problems.
rm -f run_all.done run_all.failed
bad=""
chk(){ f=$1; want=$2; last=$(tail -n 1 "$f" 2>/dev/null); if [ "$last" != "rc=$want" ]; then bad="$bad $f(want rc=$want, got '$last')"; fi; }
chk CV6_A_local_linear.out 0; chk CV6_A_local_linear_MUTATE_a.out 1; chk CV6_A_local_linear_MUTATE_b.out 1
chk CV6_B_layers.out 1; chk CV6_B_layers_MUTATE_a.out 1; chk CV6_B_layers_MUTATE_b.out 1
chk CV6_C_switched_stiffness.out 0; chk CV6_C_switched_stiffness_MUTATE_k.out 1
chk CV6_D_T3_sensitivity.out 0; chk CV6_D_T3_sensitivity_MUTATE_x30.out 1
if [ -z "$bad" ]; then echo ALLDONE > run_all.done; else echo "INCOMPLETE:$bad" > run_all.failed; fi
