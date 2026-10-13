#!/bin/bash
# CFG720 waiter (FROZEN_CRITERIA.md section 5): start only when no 1024^3 PM job or other merger lane is live and >= 16 GB is free.
# Usage: nohup bash campaign_fresh_gravity/CFG720_one_action_merger_window/run_720.sh &
HERE="$(cd "$(dirname "$0")" && pwd)"
LOG="$HERE/../../../_external_data/cfg720_work/waiter.log"; mkdir -p "$(dirname "$LOG")"
free_gb() { vm_stat | awk '/page size of/ {ps=$8} /Pages free/ {f=$3} /Pages inactive/ {i=$3} END {gsub("\\.","",f); gsub("\\.","",i); printf "%d", (f+i)*ps/1e9}'; }
while true; do
  if pgrep -f "_pm.py|run_636.py|run_596.py|run_640.py|cfg639_merger.py|cfg641.py" > /dev/null; then
    echo "$(date '+%F %T') heavy job live; waiting" >> "$LOG"; sleep 600; continue
  fi
  fg=$(free_gb)
  if [ "$fg" -lt 16 ]; then echo "$(date '+%F %T') free ${fg} GB < 16; waiting" >> "$LOG"; sleep 600; continue; fi
  echo "$(date '+%F %T') starting CFG720 (free ${fg} GB)" >> "$LOG"
  cd "$HERE" && OMP_NUM_THREADS=1 nice -n 10 python3 cfg720.py >> "$LOG" 2>&1
  echo "$(date '+%F %T') CFG720 exit $?" >> "$LOG"
  break
done
