#!/bin/bash
# BK2 watcher: nice 19, idle loop. Every 30 min writes bk2_status.out from the logs. When a level's harvest finishes for a footing and mode, runs bk2_stage2.py on it. Writes SURVIVOR_FLAG if any all-line cheap pass appears. Commits nothing, sends nothing.
cd "$(dirname "$0")"; export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1
while :; do
  { date; for l in bk2_*_L?.log; do echo "$l: $(tail -1 "$l" | cut -c1-230)"; done; du -sh chunks; df -h . | tail -1; } > bk2_status.out
  for m in alt_control:L1 canonical_control:L1 alt_real:L2 canonical_real:L2 alt_control:L2 canonical_control:L2; do f=${m%%:*}; lev=${m##*:}; fo=${f%%_*}; mo=${f##*_}
    if [ -f chunks/${lev}_${f}/READ ] && [ ! -f bk2_stage2_${lev}_${fo}_${mo}.json ]; then nice -n 19 python3 bk2_stage2.py $fo $mo $lev > bk2_stage2_${lev}_${fo}_${mo}.out 2>&1; grep -q "all cheap LINE [1-9]" bk2_stage2_${lev}_${fo}_${mo}.out && touch SURVIVOR_FLAG; fi; done
  [ -f chunks/driver_alt.done ] && [ -f chunks/driver_canonical.done ] && [ -f bk2_stage2_L2_canonical_control.json ] && break
  /bin/sleep 1800
done; echo finished >> bk2_status.out
