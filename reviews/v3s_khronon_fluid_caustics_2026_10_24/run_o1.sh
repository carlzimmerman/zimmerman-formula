#!/bin/bash
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
jobs=(); for foot in canonical alt; do for ti in 3 6 9; do jobs+=("--mode sc --foot $foot --orbit O1 --ti $ti --h 10 --extend"); done; done
run_stream() { for ((k=$1; k<${#jobs[@]}; k+=3)); do nice -n 15 python3 khronon_fluid.py ${jobs[$k]} >> logs/o1_$1.log 2>&1; echo "done $k rc $?" >> logs/o1_$1.log; done; }
run_stream 0 & run_stream 1 & run_stream 2 & wait
