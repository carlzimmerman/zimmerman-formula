#!/bin/bash
# usage: run.sh <python-script> [args...]   (1 thread, nice 19, wall/RSS via /usr/bin/time)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1
PY=/Applications/Xcode.app/Contents/Developer/usr/bin/python3
exec nice -n 19 /usr/bin/time -l "$PY" "$@"
