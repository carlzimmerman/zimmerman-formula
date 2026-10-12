#!/bin/bash
# CFG636 production waiter (FROZEN_CRITERIA.md section 2, 89aeaae12).  Kills nothing, signals nothing.
# Polls every 2 min until (a) no cfg596_pm.py process is running, (b) no cfg636_pm.py process is running, and
# (c) free + inactive memory >= 42 GB; then starts the CFG636 canonical production job C1 (H-CB RES canonical, 1024^3 L100)
# detached with nohup under nice 10, and exits.  A copy runs from _external_data/cfg636_work/ (log: cfg636_waiter.log there).
# Started with:  nohup bash _external_data/cfg636_work/cfg636_waiter.sh > /dev/null 2>&1 &
HERE="$(cd "$(dirname "$0")" && pwd)"
RUNNER="${CFG636_RUNNER:-$(ls "$HERE"/../../*/campaign_fresh_gravity/CFG636_hcb_native_1024/run_636.py 2>/dev/null | head -1)}"
LOG="$HERE/cfg636_waiter.log"
NEED_GB=42
echo "$(date '+%Y-%m-%d %H:%M:%S') waiter start pid $$; runner $RUNNER; need no cfg596_pm.py / cfg636_pm.py process and free+inactive >= ${NEED_GB} GB" >> "$LOG"
[ -f "$RUNNER" ] || { echo "$(date '+%F %T') runner not found, exiting" >> "$LOG"; exit 1; }
while true; do
  # count only processes whose executable is python and whose script argument is the engine (never a shell that mentions it)
  N596=$(ps -axo command= | awk '$1 ~ /python/ && $2 ~ /cfg596_pm[.]py$/' | wc -l | tr -d ' ')
  N636=$(ps -axo command= | awk '$1 ~ /python/ && $2 ~ /cfg636_pm[.]py$/' | wc -l | tr -d ' ')
  FI=$(vm_stat | awk '/page size of/{ps=$8}/Pages free/{f=$3}/Pages inactive/{i=$3}END{gsub("\\.","",f);gsub("\\.","",i);printf "%.1f",(f+i)*ps/1e9}')
  echo "$(date '+%Y-%m-%d %H:%M:%S') cfg596_pm procs $N596 cfg636_pm procs $N636 free+inactive ${FI} GB" >> "$LOG"
  if [ "$N596" = "0" ] && [ "$N636" = "0" ] && awk -v x="$FI" -v n="$NEED_GB" 'BEGIN{exit !(x+0 >= n)}'; then
    cd "$(dirname "$RUNNER")" || exit 1
    nohup nice -n 10 python3 "$RUNNER" serial C1 > "$HERE/run_636_C1_nohup.log" 2>&1 &
    echo "$(date '+%Y-%m-%d %H:%M:%S') LAUNCHED run_636.py serial C1 (pid $!); waiter exits" >> "$LOG"
    exit 0
  fi
  sleep 120
done
