#!/bin/bash
# EFN1 driver: waits for the BX1 queue to finish, then runs the lane's batches one at a time at nice 19, 4 threads at most.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4
until ! pgrep -f "bx1_pm.py|bx1_run.py" >/dev/null; do sleep 120; done
echo "start $(date)"; uptime; df -g . | tail -1
nice -n 19 python3 -W ignore efn1_route_w.py 2 3 > /dev/null 2>efn1_err_w.txt; echo "route W R2 R3 done $(date)"
for b in main ka kab2 mutate ext; do nice -n 19 python3 -W ignore efn1_route_d.py $b > /dev/null 2>efn1_err_$b.txt; echo "$b done $(date)"; done
nice -n 19 python3 -W ignore efn1_route_d.py frozen > /dev/null 2>efn1_err_frozen.txt; echo "frozen done $(date)"
EFN1_DIM=3 nice -n 19 python3 efn1_sympy.py > /dev/null 2>efn1_err_sympy.txt; echo "sympy 3D done $(date)"
echo "end $(date)"
