#!/bin/bash
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OPENBLAS_NUM_THREADS=1 CFG102_BC=N
( time python3 cfg102_b_scan.py > cfg102_b_BCN.out 2>&1 ) 2> bN_time.txt
( time python3 cfg102_c_attack.py > cfg102_c_BCN.out 2>&1 ) 2> cN_time.txt
