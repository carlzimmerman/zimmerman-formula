#!/bin/bash
# Sequential (one process at a time): axial derivation, TF limit + hydro anchor, compact-control sign check,
# GR continuation one Gamma per process (20 min cap each via perl alarm).
cd "$(dirname "$0")"
CAP="perl -e alarm(shift);exec(@ARGV) 1200"
mkdir -p results/axial results/compact results/gr
$CAP ./run.sh axial_master.py ../../full_two_field_2026_10_19/equilibria/mixed_G1em8_x04.npz results/axial/axial.json > results/axial/axial.stdout 2> results/axial/axial.time
$CAP ./run.sh tf_limit.py results/tf_limit.json > results/tf_limit.stdout 2> results/tf_limit.time
CSEED=../../full_two_field_2026_10_19/equilibria/run_001/mixed_center.npz
$CAP ./run.sh nr_gpp.py --gamma 8.5e-5 --center x --value 0.02 --seed $CSEED --N 1500 --rbox 600 --ls 0,1,2 --vk --coercivity --out results/compact/nr_R600_N1500 > results/compact/N1500.stdout 2> results/compact/N1500.time
$CAP ./run.sh nr_gpp.py --gamma 8.5e-5 --center x --value 0.02 --seed $CSEED --N 2399 --rbox 600 --ls 0 --vk --out results/compact/nr_R600_N2399 > results/compact/N2399.stdout 2> results/compact/N2399.time
$CAP ./run.sh nr_gpp.py --gamma 8.5e-5 --center x --value 0.02 --seed $CSEED --N 1500 --rbox 450 --ls 0 --out results/compact/nr_R450_N1500 > results/compact/R450.stdout 2> results/compact/R450.time
SEED=../../full_two_field_2026_10_19/equilibria/mixed_G1em8_x04.npz
k=0
for G in 1e-8 3.1623e-9 1e-9 3.1623e-10 1e-10 3.1623e-11 1e-11 3.1623e-12 1e-12; do
  $CAP ./run.sh gr_continue.py --gammas $G --seed $SEED --out results/gr/continue_$k > results/gr/continue_$k.stdout 2> results/gr/continue_$k.time
  nxt=$(ls results/gr/continue_${k}_G*.npz 2>/dev/null | head -1)
  if [ -z "$nxt" ]; then echo "stop at $G" > results/gr/STOPPED; break; fi
  SEED=$nxt; k=$((k+1))
done
echo done > results/SEQ2_DONE
