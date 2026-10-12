#!/bin/bash
# CFG640 production waiter (FROZEN_CRITERIA.md section 3, 71b2cc1c9).  Kills nothing, signals nothing.  NOT started by the lane's
# author: the owner / orchestrator starts it once they choose to queue CFG640 behind CFG636.
# Polls every 2 min until ALL hold:
#   (a) CFG636 C1 is finished AND scored: CFG636_hcb_native_1024/cfg636_native_results.json exists and contains a canonical run;
#   (b) no cfg596_pm.py, cfg636_pm.py or cfg640_pm.py engine process is running;
#   (c) free + inactive memory >= 48 GB;
# then starts run_640.py serial H1 (phase RES canonical, 1024^3 L100) detached with nohup under nice 10, and exits.
# Start (from the repository root):  nohup bash campaign_fresh_gravity/CFG640_phase_source_pm/cfg640_waiter.sh > /dev/null 2>&1 &
HERE="$(cd "$(dirname "$0")" && pwd)"
RUNNER="$HERE/run_640.py"
SCORED="$HERE/../CFG636_hcb_native_1024/cfg636_native_results.json"
WORK="$(cd "$HERE/../../.." && pwd)/_external_data/cfg640_work"
mkdir -p "$WORK"; LOG="$WORK/cfg640_waiter.log"
NEED_GB=48
echo "$(date '+%Y-%m-%d %H:%M:%S') waiter start pid $$; need CFG636 scored, no engine process, free+inactive >= ${NEED_GB} GB" >> "$LOG"
while true; do
  N=$(ps -axo command= | awk '$1 ~ /python/ && $2 ~ /cfg(596|636|640)_pm[.]py$/' | wc -l | tr -d ' ')
  FI=$(vm_stat | awk '/page size of/{ps=$8}/Pages free/{f=$3}/Pages inactive/{i=$3}END{gsub("\\.","",f);gsub("\\.","",i);printf "%.1f",(f+i)*ps/1e9}')
  SC=0
  if [ -f "$SCORED" ] && python3 -c "import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if any(r.get('foot')=='canonical' for r in d.get('runs',{}).values()) and not d.get('mutate') else 1)" "$SCORED"; then SC=1; fi
  echo "$(date '+%Y-%m-%d %H:%M:%S') cfg636 scored $SC engine procs $N free+inactive ${FI} GB" >> "$LOG"
  if [ "$SC" = "1" ] && [ "$N" = "0" ] && awk -v x="$FI" -v n="$NEED_GB" 'BEGIN{exit !(x+0 >= n)}'; then
    cd "$HERE" || exit 1
    nohup nice -n 10 python3 "$RUNNER" serial H1 > "$WORK/run_640_H1_nohup.log" 2>&1 &
    echo "$(date '+%Y-%m-%d %H:%M:%S') LAUNCHED run_640.py serial H1 (pid $!); waiter exits" >> "$LOG"
    exit 0
  fi
  sleep 120
done
