#!/bin/bash
# AC15: run every hydro case, 4 at a time, one thread each, nice 10. Rerun resumes from checkpoints.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONHASHSEED=0
mkdir -p logs
while read -r line; do echo "$line"; done < runlist.txt | xargs -P 4 -I{} sh -c 'nice -n 10 python3 -B hydro.py {} > "logs/$(echo {} | tr -d " -" ).log" 2>&1'
echo ALLDONE
