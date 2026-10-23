#!/bin/bash
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
for a in "v1a" "v1b 1" "v1b 2" "v2"; do /usr/bin/time -l nice -n 15 python3 x1_validation.py $a 2>&1 | grep -vE "Warning|^ +[a-z]" | grep -E "max_err|maximum resident|real|Pabs|exact|\{" ; done
echo V12 DONE
