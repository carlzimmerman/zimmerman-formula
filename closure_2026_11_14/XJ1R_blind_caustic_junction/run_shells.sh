#!/bin/bash
# XJ1R (FROZEN_CRITERIA.md section 9): the 24 light shell runs (FLD1's 12 masses x 2 footings), 6 at a time, nice 19,
# single thread each; finished runs are skipped. Writes runs/*.json and logs/shells.log; touches logs/shells.done.
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
cd "$(dirname "$0")"; mkdir -p runs logs
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1
for f in canonical alt; do for m in 12 11.5 11.2 10.9 10.7 10.45 10 9.4 9 8 7 6.5; do
  [ -f runs/hubble_${f}_M${m}_zi10_N2400.json ] || echo "$f $m"; done; done |
  xargs -P 6 -L 1 sh -c 'nice -n 19 python3 -I -B xj1r_shells.py --footing $0 --logMb $1' >> logs/shells.log 2>&1
n=$(ls runs/hubble_*_zi10_N2400.json 2>/dev/null | wc -l | tr -d ' ')
echo "runs on disk: $n ($(date +%H:%M))" >> logs/shells.log
[ "$n" -eq 24 ] && touch logs/shells.done
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
