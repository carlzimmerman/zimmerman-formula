#!/usr/bin/env bash
# unattended_depth10.sh — run the whole depth-10 exhaustive push with no supervision.
#
# Sequence, with a hard safety gate between steps:
#   1. wait for the in-flight depth-8 sharded validation to finish
#   2. ONLY IF it printed "VALIDATION PASSED", launch the 12-shard depth-10 build in parallel
#   3. when all 12 shards land, merge them
#   4. write STATUS.txt at every transition so the whole run can be read in one shot later
# If validation FAILED or is inconclusive, it stops and says so. It never runs a multi-hour exhaustive
# build on unvalidated code -- the first validation attempt lost 19% of depth 8's distinct values to a
# float64 re-keying bug, which is exactly the failure this gate exists to catch.
set -uo pipefail
cd "$(dirname "$0")"

ST="results_grind/depth_10/STATUS.txt"
mkdir -p results_grind/depth_10
say(){ echo "[$(date '+%F %T')] $*" >> "$ST"; }

say "orchestrator start; waiting on depth-8 sharded validation"

# ---- 1. wait for validation (bounded: 2 h is far beyond its ~12 min cost)
for _ in $(seq 1 480); do
  grep -qE "VALIDATION (PASSED|FAILED)" /tmp/val8b.log 2>/dev/null && break
  pgrep -f "sharded_build.py --validate" >/dev/null || break
  sleep 15
done

if grep -q "VALIDATION PASSED" /tmp/val8b.log 2>/dev/null; then
  say "depth-8 validation PASSED -- sharded path reproduces the committed serial counts"
elif grep -q "VALIDATION FAILED" /tmp/val8b.log 2>/dev/null; then
  say "depth-8 validation FAILED -- STOPPING. Do not trust the sharded path. See /tmp/val8b.log"
  cp /tmp/val8b.log "results_grind/depth_10/validation_FAILED.log" 2>/dev/null
  exit 1
else
  say "validation inconclusive (no verdict line, process gone) -- STOPPING rather than guessing"
  cp /tmp/val8b.log "results_grind/depth_10/validation_inconclusive.log" 2>/dev/null
  exit 1
fi

# ---- 2. launch the depth-10 shards
N=12
say "launching $N depth-10 shards"
for i in $(seq 0 $((N-1))); do
  nohup caffeinate -s python3 sharded_build.py --depth 10 --shard "$i" --nshards "$N" \
    > "results_grind/depth_10/shard${i}.log" 2>&1 &
done
say "all $N shards launched"

# ---- 3. wait for every shard, then merge
SD="results_grind/depth_10/shards"
for _ in $(seq 1 2880); do          # up to 24 h
  n=$(ls "$SD"/meta_shard*of${N}.json 2>/dev/null | wc -l | tr -d ' ')
  [ "$n" -ge "$N" ] && break
  pgrep -f "sharded_build.py --depth 10" >/dev/null || { say "WARNING: no shard processes alive but only $n/$N metas -- some shard died; see shard*.log"; break; }
  sleep 30
done

n=$(ls "$SD"/meta_shard*of${N}.json 2>/dev/null | wc -l | tr -d ' ')
if [ "$n" -lt "$N" ]; then
  say "only $n/$N shards completed -- NOT merging (a partial union would be a FALSE null)"
  exit 1
fi
say "all $N shards complete; merging"
python3 sharded_build.py --depth 10 --merge --nshards "$N" >> "results_grind/depth_10/merge.log" 2>&1
if [ $? -eq 0 ]; then
  say "MERGE DONE. Result:"
  python3 - <<'PY' >> "results_grind/depth_10/STATUS.txt" 2>&1
import json
m = json.load(open("results_grind/depth_10/build_meta_sharded.json"))
print(f"    depth 10 EXHAUSTIVE: raw={m['raw_candidates']:,} distinct={m['distinct_by_value']:,}")
print( "    NOTE: this is the VALUE SET only. The target sweep + VERDICT.json have NOT been run,")
print( "    so this says NOTHING yet about whether anything matches an SM target.")
PY
else
  say "merge FAILED -- see merge.log"
fi
say "orchestrator done"
