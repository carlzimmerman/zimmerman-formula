#!/bin/bash
# AN2 diagnostic SL: all runs, two at a time, nice 15, one thread
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONUNBUFFERED=1
printf '%s\n' "D0 1e15 64" "D0 1e12 64" "D0 1e15 128" "D0 1e12 128" "D1 1e15 128" "D1 1e12 128" \
  "D2 1e15 128" "D2 1e12 128" "D3 1e15 128" "D3 1e12 128" "D4 1e15 160" "D4 1e12 160" |
  xargs -P 2 -L 1 sh -c 'nice -n 15 python3 sphere_lag.py $0 $1 $2'
