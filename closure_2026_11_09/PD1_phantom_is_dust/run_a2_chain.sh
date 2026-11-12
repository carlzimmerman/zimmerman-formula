#!/bin/bash
# PD1 A2 readings through pd1_a1.py: galaxy basin share 5.41 x f_basin (2.0 graded; 1.8, 2.2 brackets); clusters 5.41 with prefactor 1 (bracket)
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1
for S in 10.82 9.738 11.902; do PD1_SHARE=$S nice -n 10 python3 pd1_a1.py > run_pd1_a1_share$S.txt 2>&1 || echo "FAILED share $S"; done
PD1_SHARE=5.41 PD1_FCPRE=1.0 nice -n 10 python3 pd1_a1.py > run_pd1_a1_share5.41_fcpre1.0.txt 2>&1 || echo "FAILED fcpre"
echo "[chain] done"
