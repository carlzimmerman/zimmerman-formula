#!/bin/bash
# h = 10 rung: cases listed in summary.json["rung_cases"] (frozen selection rule), three single-thread streams
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
jobs=()
while IFS= read -r line; do jobs+=("$line"); done < <(python3 -c "
import json
for f,o,t in json.load(open('summary.json'))['rung_cases']:
    print(f'--mode sc --foot {f} --orbit {o} --ti {t} --h 10 --extend')")
run_stream() { for ((k=$1; k<${#jobs[@]}; k+=3)); do nice -n 15 python3 khronon_fluid.py ${jobs[$k]} >> logs/rung$1.log 2>&1; echo "done $k rc $?" >> logs/rung$1.log; done; }
run_stream 0 & run_stream 1 & run_stream 2 & wait
echo RUNG_DONE >> logs/batch.log
