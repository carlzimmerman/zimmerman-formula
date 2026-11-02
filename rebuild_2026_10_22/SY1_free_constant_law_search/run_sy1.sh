#!/bin/bash
# SY1 full run, per AMENDMENT_A1: starts at once beside BF1, 8 one-core searches at nice 10. Planted, then real, scrambled, mutate. sy1.py yields to 1024^3 runs and compute_queue jobs and restarts when clear; a rerun of this script resumes.
# Ends by writing sy1_search.done. Only planted is read here, since controls read first. kappa = 1/2 FITTED; not theory closed.
cd "$(dirname "$0")"; ITERS=${SY1_ITERS:-1500}; SLICE=${SY1_SLICE:-20}; NW=${SY1_WORKERS:-8}
trap 'kill -TERM $CUR 2>/dev/null; wait $CUR 2>/dev/null; echo "$(date +%m-%d\ %H:%M:%S) run_sy1: SIGTERM, checkpointed; rerun resumes"; exit 75' TERM INT
echo "$(date +%m-%d\ %H:%M:%S) run_sy1: iters $ITERS slice $SLICE workers $NW"
rc=""
for m in planted real scrambled mutate; do
  python3 sy1.py "$m" --iters "$ITERS" --slice "$SLICE" --maxw "$NW" --fixed --ramp 20 & CUR=$!; wait $CUR; r=$?; rc="$rc $m:$r"
  echo "$(date +%m-%d\ %H:%M:%S) run_sy1: $m exit $r"
  [ "$m" = planted ] && { python3 sy1_read.py planted & CUR=$!; wait $CUR; }
done
echo "search finished$rc $(date +%F\ %T)" > sy1_search.done
echo "$(date +%m-%d\ %H:%M:%S) run_sy1: wrote sy1_search.done:$rc"
