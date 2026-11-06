#!/bin/bash
# AC24: hydro runs, 4 at a time, one thread each, nice 15; resumable from checkpoints (hydro's SIGTERM handler).
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONHASHSEED=0
mkdir -p logs
cat runlist.txt | xargs -P 4 -I{} sh -c 'nice -n 15 python3 -B hydro_ac24.py {} > "logs/$(echo {} | tr -d " -" ).log" 2>&1'
echo ALLDONE
