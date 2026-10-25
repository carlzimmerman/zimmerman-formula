#!/bin/bash
# X48 direct launch (owner 10-25: "keep it cranking"): six small single-thread runs, nice 15, same work dirs as the queued jobs
cd "$(dirname "$0")/../.."
L=rebuild_2026_10_22/X48_native_cf_zoom
pids=()
for spec in "1e14 1" "1e14 2" "1e14 3" "1e13 1" "1e13 2" "1e13 3"; do
  set -- $spec; W=$L/runs/M$1_s$2_ng38; mkdir -p $W
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 15 python3 $L/x48_zoom.py --mass $1 --seed $2 --ng 38 --work $W --resume > $W/run.log 2>&1 &
  pids+=($!)
done
trap 'kill -TERM "${pids[@]}" 2>/dev/null; wait; exit 75' TERM INT
wait
echo "all six finished"
