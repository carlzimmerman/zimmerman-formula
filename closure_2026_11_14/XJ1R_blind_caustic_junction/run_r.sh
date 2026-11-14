#!/bin/bash
# XJ1R heavy forest stage (FROZEN_CRITERIA.md sections 4 and 9). One part process at a time, nice 19, 3 flux threads, FWN1's
# footprint guard (exit 76 above 14 GB physical footprint; the part is restarted and resumes from its box files).
# A part starts only when at most two other heavy forest processes are alive (command lines containing xj1b_run.py,
# xj1b2_run.py, xj1a_run.py, fwn2a_run.py, fwn2b_run.py or xj1r_run.py; the counting awk excludes itself) and free disk is
# >= 10 GB (else wait 60 s). STOP (runner exits) when free disk < 8 GB or swap used > 14 GB, checked before every start and
# every 30 s while a part runs (the part gets SIGTERM and stops between boxes, exit 75). Restartable: finished parts are
# skipped. Writes run_r.done when the last part is done. Needs tmp/tables_z*.npz (built by xj1r_tables.py beforehand).
# Launch: nohup ./run_r.sh >> logs/run_r.log 2>&1 &   (pid in logs/run_r.pid)
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
cd "$(dirname "$0")"; mkdir -p logs
echo $$ > logs/run_r.pid
export XJ1R_THREADS=3 XJ1R_MEM_GB=16 XJ1R_FOOT_GB=14
heavy_n() { ps -axo command= | awk 'tolower($0) ~ /python/ && /(xj1b_run|xj1b2_run|xj1a_run|fwn2a_run|fwn2b_run|xj1r_run)\.py/ && !/awk/' | wc -l | tr -d ' '; }
disk_gb() { df -g . | awk 'NR==2 {print $4}'; }
swap_mb() { sysctl -n vm.swapusage | sed -E 's/.*used = ([0-9.]+)M.*/\1/'; }
bad() {
  local a s; a=$(disk_gb); s=$(swap_mb)
  if [ "$a" -lt 8 ]; then echo "STOP: free disk ${a} GB below 8 GB ($(date +%H:%M))"; return 0; fi
  if [ "$(echo "$s > 14336" | bc)" -eq 1 ]; then echo "STOP: swap used ${s} MB above 14 GB ($(date +%H:%M))"; return 0; fi
  return 1
}
guard() {
  while true; do
    if bad; then exit 3; fi
    local a n; a=$(disk_gb); n=$(heavy_n)
    if [ "$a" -ge 10 ] && [ "$n" -le 2 ]; then echo "guard ok: disk ${a} GB, swap $(swap_mb) MB, other heavy ${n} ($(date +%H:%M))"; return 0; fi
    echo "  waiting: disk ${a} GB, other heavy ${n} ($(date +%H:%M))"; sleep 60
  done
}
part() {
  local tag="$1_z$2_s$3_$4"
  [ -f "parts/${tag}.json" ] && return 0
  while true; do
    guard
    echo "start ${tag} ($(date +%H:%M))"
    nice -n 19 python3 -I -B xj1r_run.py "$@" & local pid=$!
    while kill -0 $pid 2>/dev/null; do
      if bad; then kill -TERM $pid; wait $pid; echo "stopped ${tag} by the disk/swap guard"; exit 4; fi
      sleep 30
    done
    wait $pid; local rc=$?
    if [ $rc -eq 0 ]; then echo "done ${tag} ($(date +%H:%M))"; return 0
    elif [ $rc -eq 76 ]; then echo "restart ${tag} (rc 76)"; continue
    else echo "stopped rc $rc at ${tag}"; exit $rc; fi
  done
}
for s in 0 1 2 3 4 5 6 7 8 9 10 11; do for f in canonical alt; do part prim 2.2 $s $f; done; done
for z in 3.0 4.4 2.6 3.4 3.8; do for f in canonical alt; do part oz $z 0 $f; done; done
for f in canonical alt; do part bracketF 2.2 0 $f; done
for f in canonical alt; do part clusteredF 2.2 0 $f; done
for f in canonical alt; do part bracketF 3.0 0 $f; done
n=$(ls parts/*.json 2>/dev/null | wc -l | tr -d ' ')
echo "parts on disk: $n of 40 ($(date +%H:%M))"
[ "$n" -eq 40 ] && touch run_r.done
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
