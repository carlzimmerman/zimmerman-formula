#!/bin/bash
# B3: bounded reruns of Codex's crossing_base (n128) and ultra (n512) from copied code, Codex's recorded argv.
cd "$(dirname "$0")/../cg_copy"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
for job in "crossing_base gas_v3.py 128" "ultra gas_v4.py 512"; do
  set -- $job
  start=$(date +%s)
  /usr/bin/time -l timeout 600 nice -n 15 arch -arm64 /usr/bin/python3 $2 --output ../cg_rerun/$1_result.json --n $3 --zend 8 \
     > ../cg_rerun/$1_stdout.txt 2> ../cg_rerun/$1_stderr.txt
  echo "$1 exit $? wall $(( $(date +%s) - start )) s" >> ../cg_rerun/RUNLOG.txt
done
