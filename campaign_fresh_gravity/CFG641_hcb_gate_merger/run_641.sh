#!/bin/bash
# CFG641 waiter (renumbered from CFG640) (FROZEN_CRITERIA.md section 5): start only after CFG639 Part B has finished, with no 1024^3 run live and >= 16 GB free.
# Usage: nohup bash campaign_fresh_gravity/CFG641_hcb_gate_merger/run_641.sh &
HERE="$(cd "$(dirname "$0")" && pwd)"
LOG="$HERE/../../../_external_data/cfg641_work/waiter.log"; mkdir -p "$(dirname "$LOG")"
L639="$HERE/../../../_external_data/cfg639_work/waiter.log"
free_gb() { vm_stat | awk '/page size of/ {ps=$8} /Pages free/ {f=$3} /Pages inactive/ {i=$3} END {gsub("\\.","",f); gsub("\\.","",i); printf "%d", (f+i)*ps/1e9}'; }
while true; do
  if ! grep -q "Part B exit" "$L639" 2>/dev/null; then echo "$(date '+%F %T') CFG639 Part B not finished; waiting" >> "$LOG"; sleep 600; continue; fi
  if pgrep -f "cfg636_pm.py|cfg596_pm.py|run_636.py|run_596.py|cfg639_merger.py" > /dev/null; then
    echo "$(date '+%F %T') heavy run live; waiting" >> "$LOG"; sleep 600; continue
  fi
  fg=$(free_gb)
  if [ "$fg" -lt 16 ]; then echo "$(date '+%F %T') free ${fg} GB < 16; waiting" >> "$LOG"; sleep 600; continue; fi
  echo "$(date '+%F %T') starting CFG641 (free ${fg} GB)" >> "$LOG"
  cd "$HERE" && OMP_NUM_THREADS=1 nice -n 10 python3 cfg641.py >> "$LOG" 2>&1
  echo "$(date '+%F %T') CFG641 exit $?" >> "$LOG"
  break
done
