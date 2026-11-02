#!/bin/bash
# HF1 gate 1: primary six m, then reported variants. Rerun resumes from cells_g1 and CLASS's own checkpoints.
cd "$(dirname "$0")"; export PYTHONHASHSEED=0 OMP_NUM_THREADS=1
P="nice -n 10 python3 -I hf1_g1.py"
for s in FD COLD CHI; do for m in 11.8 11 9 7 5 3.74; do
  if [ $s = CHI ] && [ $m = 5 -o $m = 3.74 ]; then continue; fi
  $P fit $s $m 2>&1 | grep -v -i warn; $P pk $s $m 2>&1 | grep -v -i warn; $P grade 2>&1 | tail -1
done; done; echo ALLDONE
