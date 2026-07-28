#!/usr/bin/env bash
# Build the expensive skeleton layers ONCE, in parallel, then merge. b_s<=4 are cheap; 5 and 6 are not.
set -uo pipefail
cd "$(dirname "$0")"
N=${1:-10}
for BS in 5 6; do
  echo "=== layer b_s=$BS across $N workers $(date '+%T') ===" >> results_grind/skeleton_cache.log
  for w in $(seq 0 $((N-1))); do
    nohup caffeinate -s python3 parallel_skeleton_layer.py --bs $BS --worker $w --nworkers $N \
      >> results_grind/skeleton_cache.log 2>&1 &
  done
  wait
  python3 parallel_skeleton_layer.py --bs $BS --merge --nworkers $N >> results_grind/skeleton_cache.log 2>&1
  echo "=== layer b_s=$BS MERGED $(date '+%T') ===" >> results_grind/skeleton_cache.log
done
echo "=== ALL LAYERS CACHED $(date '+%T') ===" >> results_grind/skeleton_cache.log
