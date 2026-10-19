#!/bin/bash
# Retry below 3.16e-11 with collocation tol 5e-7 (declared acceptance: rms residual <= 1e-6), 60k-node cap.
cd "$(dirname "$0")"
CAP="perl -e alarm(shift);exec(@ARGV) 1200"
SEED=$(ls results/gr/continue_5_G*.npz | head -1)
k=6
for G in 1.7783e-11 1e-11 5.6234e-12 3.1623e-12; do
  $CAP ./run.sh gr_continue.py --gammas $G --seed $SEED --tol 5e-7 --out results/gr/continue_$k > results/gr/continue_$k.stdout 2> results/gr/continue_$k.time
  nxt=$(ls results/gr/continue_${k}_G*.npz 2>/dev/null | head -1)
  if [ -z "$nxt" ]; then echo "stop at $G (tol 5e-7)" > results/gr/STOPPED; break; fi
  SEED=$nxt; k=$((k+1))
done
echo done > results/SEQ5_DONE
