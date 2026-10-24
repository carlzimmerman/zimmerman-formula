#!/bin/bash
# h = 20 production: 12 sc + 12 mutate + 3 frozen-F, three single-thread streams
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
jobs=()
for mode in sc mutate; do for foot in canonical alt; do for orb in O1 O2; do for ti in 3 6 9; do
  jobs+=("--mode $mode --foot $foot --orbit $orb --ti $ti --extend"); done; done; done; done
for ti in 3 6 9; do jobs+=("--mode frozen --foot canonical --orbit O2 --ti $ti --extend"); done
run_stream() { for ((k=$1; k<${#jobs[@]}; k+=3)); do nice -n 15 python3 khronon_fluid.py ${jobs[$k]} >> logs/stream$1.log 2>&1; echo "done $k rc $?" >> logs/stream$1.log; done; }
mkdir -p logs; rm -f runs/sc_canonical_O2_ti3_h20.json
run_stream 0 & run_stream 1 & run_stream 2 & wait
echo ALL_DONE >> logs/batch.log
