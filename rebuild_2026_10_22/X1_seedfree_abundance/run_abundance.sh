#!/bin/bash
# Abundance chain worker: runs every k-th line (k = worker index of W) of abundance/jobs.txt.
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
w=$1; W=$2; i=0
while read -r line; do
  if [ $((i % W)) -eq $w ]; then tag=${line##*--tag }; [ -f abundance/$tag.json ] || { nice -n 15 timeout 1500 python3 -W ignore x1_abundance.py $line 2>&1 | tail -1; }; fi
  i=$((i+1))
done < abundance/jobs.txt
echo "WORKER $w DONE"
