#!/bin/bash
# Re-run door 10 (CFG124) in place: main runs then MUTATE a, b, c, 1 for every script.  ZF_REPO = repository checkout (else the script walks up from its own location).
# Order matters: T0 -> G1 -> G2 -> G3 -> G4/G5 (G2 reads T0's and G1's results, G4/G5 read T0's and G2's).  G1 takes about 10-15 minutes per mode (random + Nelder-Mead search).
cd "$(dirname "$0")"
for m in "" a b c 1; do
  for s in CFG124_T0_field_equations CFG124_G1_target CFG124_G2_growth CFG124_G3_reaction_energy CFG124_G4_G5_constants_wellposed; do
    MUTATE=$m python3 $s.py > /dev/null 2>&1; echo "$s MUTATE='$m' rc=$?"
  done
done
