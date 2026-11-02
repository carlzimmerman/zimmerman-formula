#!/bin/bash
# UX7 full run order. One thread, nice 15.
export PYTHONHASHSEED=0 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
nice -n 15 python3 ux7_mass.py; nice -n 15 python3 ux7_fit.py; nice -n 15 python3 ux7_fit.py --mutate; nice -n 15 python3 ux7_grade.py; nice -n 15 python3 ux7_read.py; nice -n 15 python3 ux7_post.py
