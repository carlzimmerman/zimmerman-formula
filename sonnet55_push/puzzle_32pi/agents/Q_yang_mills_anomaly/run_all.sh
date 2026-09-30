#!/bin/bash
# Reproduce every Q-lane result (pure sympy/numpy/scipy). Exit code 0 = every check and control behaves.
cd "$(dirname "$0")"
rc=0
for s in q01_bpst_unit_and_32pi_ledger q02_beta_anomaly_condensate q03_hbar_bookkeeping_operator_link q04_s4_instanton_density_vs_rho_lambda q05_magnitude_route; do
  python3 $s.py > $s.out 2>&1 || rc=1
  echo "$s: $(tail -1 $s.out)"
done
exit $rc
