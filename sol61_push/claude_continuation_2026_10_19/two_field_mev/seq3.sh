#!/bin/bash
# GR continuation in Gamma at fixed f_c, one Gamma per process (20 min cap each).
cd "$(dirname "$0")"
CAP="perl -e alarm(shift);exec(@ARGV) 1200"
mkdir -p results/gr
SEED=../../full_two_field_2026_10_19/equilibria/mixed_G1em8_x04.npz
k=0
for G in 1e-8 3.1623e-9 1e-9 3.1623e-10 1e-10 3.1623e-11 1e-11 3.1623e-12 1e-12; do
  $CAP ./run.sh gr_continue.py --gammas $G --seed $SEED --out results/gr/continue_$k > results/gr/continue_$k.stdout 2> results/gr/continue_$k.time
  nxt=$(ls results/gr/continue_${k}_G*.npz 2>/dev/null | head -1)
  if [ -z "$nxt" ]; then echo "stop at $G" > results/gr/STOPPED; break; fi
  SEED=$nxt; k=$((k+1))
done
echo done > results/SEQ3_DONE
