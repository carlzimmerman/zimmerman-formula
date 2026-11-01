#!/bin/bash
# SL1 real runs: 3 at a time, one thread, nice 15. Resumes: GA checkpoints on SIGTERM (exit 75); re-run this script.
cd "$(dirname "$0")"; mkdir -p runs
go() { OMP_NUM_THREADS=1 nice -n 15 python3 -I discover_law.py "$@" > "runs/log_$(echo $* | tr -d ' -').txt" 2>&1; }
pids=(); trap 'kill -TERM "${pids[@]}" 2>/dev/null; wait; exit 75' TERM INT
( go --ga SPEC 1; go --ga SPEC 2; go --ga SPEC 3 ) & pids+=($!)
( go --ga NATIVE 1; go --ga NATIVE 2; go --ga NATIVE 3 ) & pids+=($!)
( go --sweep SPEC; go --sweep NATIVE ) & pids+=($!)
wait; echo "SL1 runs finished $(date)"
