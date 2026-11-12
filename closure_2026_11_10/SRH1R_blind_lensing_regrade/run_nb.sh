#!/bin/bash
# SRH1R: neighbour terms for one footing, every case, one thread.  Usage: run_nb.sh <work dir> <footing>
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$(dirname "$0")"
for c in f0.40 f0.50 f0.60 f0.70; do python3 -I -u srh1r_nb.py "$1" "$2" $c null || exit 1; done
for c in ref inf one1 mu1 mu2 mu3; do python3 -I -u srh1r_nb.py "$1" "$2" $c || exit 1; done
echo all > "$1/nb_$2.alldone"
