#!/bin/bash
# E1 prototype lattice runs (FROZEN_CRITERIA §2 E1, A2). Single thread, nice, each a few minutes.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
run() { job=$1; shift; [ -f lattice/$job.json ] && return; /usr/bin/time -l nice -n 15 python3 x1_lattice.py --job $job "$@" --tau-end 2000 2>&1 | grep -E "done|maximum resident|real"; }
run P32_TW_p50_s1   --N 32 --variant TW_full --patch p50 --seed 1
run P32_TW_p50_s1_dt2 --N 32 --variant TW_full --patch p50 --seed 1 --dt-div 40
run P32_TW_p50_s2   --N 32 --variant TW_full --patch p50 --seed 2
run P32_TWkc_p50_s1 --N 32 --variant TW_kc --patch p50 --seed 1
run P32_CSA_p50_s1  --N 32 --variant CSA --patch p50 --seed 1
run P32_XI16_s1     --N 32 --variant XI16 --seed 1
run P32_TW_p10_s1   --N 32 --variant TW_full --patch p10 --seed 1
run P32_TW_p90_s1   --N 32 --variant TW_full --patch p90 --seed 1
run P48_TW_p50_s1   --N 48 --variant TW_full --patch p50 --seed 1
run P64_TW_p50_s1   --N 64 --variant TW_full --patch p50 --seed 1
run P64_TWkc_p50_s1 --N 64 --variant TW_kc --patch p50 --seed 1
run P64_CSA_p50_s1  --N 64 --variant CSA --patch p50 --seed 1
run P64_TW_p50_s1_dt2 --N 64 --variant TW_full --patch p50 --seed 1 --dt-div 40
echo PROTO DONE
