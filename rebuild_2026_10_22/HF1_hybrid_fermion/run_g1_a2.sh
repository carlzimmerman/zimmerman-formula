#!/bin/bash
# HF1 AMENDMENT A2: FD at m 5, 3.74 with YHe fixed.
cd "$(dirname "$0")"; export PYTHONHASHSEED=0 OMP_NUM_THREADS=1
P="nice -n 10 python3 -I hf1_g1.py"
for m in 5 3.74; do $P fit FDY $m 2>&1 | grep -v -i warn; $P pk FDY $m 2>&1 | grep -v -i warn; done; $P grade 2>&1 | tail -3; echo A2DONE
