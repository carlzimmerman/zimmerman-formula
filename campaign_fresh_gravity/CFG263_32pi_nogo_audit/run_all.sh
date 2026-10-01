#!/bin/sh
# CFG263: rerun everything from an empty results.json, in order. Writes only inside this directory.
set -e
cd "$(dirname "$0")"
rm -f results.json
for s in cfg263_01_G_symmetry cfg263_02_E_literature cfg263_03_X1_generator_noether cfg263_04_K_density_linear \
         cfg263_05_L_sds cfg263_06_N_jacobson cfg263_07_P12_B3_horizon cfg263_08_S61_clock_bbn \
         cfg263_10_compare_originals cfg263_09_mutate cfg263_11_classify; do
  python3 "$s.py" > "$s.out" 2>&1
  echo "$s: exit 0, $(grep '^==' "$s.out" | tail -1)"
done
