#!/bin/bash
# WF1 gate 1: controls, two screens, two fits, grade. Resumes from cells/.
cd "$(dirname "$0")"; export PYTHONHASHSEED=0 OMP_NUM_THREADS=1; P="nice -n 10 python3 -I wf1_g1.py"
$P controls 2>&1 | grep -v Warning > controls.log || { echo CONTROLS_FAILED; exit 1; }
($P screen 0 2 2>&1 | grep -v Warning > scr0.log) & ($P screen 1 2 2>&1 | grep -v Warning > scr1.log) & wait
($P fit 0 2 2>&1 | grep -v Warning > fit0.log) & ($P fit 1 2 2>&1 | grep -v Warning > fit1.log) & wait
$P grade > grade.log 2>&1; echo G1DONE
