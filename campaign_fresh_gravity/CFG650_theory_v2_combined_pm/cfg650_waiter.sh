#!/bin/bash
# CFG650 production waiter (FROZEN_CRITERIA.md sections 2-3, 3087298c7).  Kills nothing, signals nothing.  CREATED, NOT STARTED by the
# lane's author: the orchestrator starts it once it has chosen the queue order versus CFG640, and applies the criteria's CFG648 clause
# by choosing the job:  CFG650_JOB=T1 (M1+M2+M3+M4, default) or CFG650_JOB=T1x (M1+M2+M3, only if CFG648 has committed a FAILS verdict
# for H-SP with the condensed-only source before launch).  Any other job name is refused.
# Polls every 2 min until ALL hold:
#   (a) no cfg596_pm.py, cfg636_pm.py, cfg640_pm.py or cfg650_pm.py engine process is running;
#   (b) free + inactive memory >= 48 GB;
# then starts run_650.py serial $CFG650_JOB detached with nohup under nice 10, and exits.
# Start (from the repository root):
#   CFG650_JOB=T1 nohup bash campaign_fresh_gravity/CFG650_theory_v2_combined_pm/cfg650_waiter.sh > /dev/null 2>&1 &
HERE="$(cd "$(dirname "$0")" && pwd)"
RUNNER="$HERE/run_650.py"
JOB="${CFG650_JOB:-T1}"
case "$JOB" in T1|T1x|T12) ;; *) echo "refused job '$JOB' (criteria section 2 + addendum A1 allow T1, T1x, T12)"; exit 1;; esac
WORK="$(cd "$HERE/../../.." && pwd)/_external_data/cfg650_work"
mkdir -p "$WORK"; LOG="$WORK/cfg650_waiter.log"
NEED_GB=48
echo "$(date '+%Y-%m-%d %H:%M:%S') waiter start pid $$ job $JOB; need no cfg596/636/640/650 engine process and free+inactive >= ${NEED_GB} GB" >> "$LOG"
if [ -f "$HERE/../CFG648_phase_mixed_settling/README.md" ]; then
  echo "$(date '+%Y-%m-%d %H:%M:%S') NOTE: CFG648 README exists; its verdict lines (apply the criteria's CFG648 clause):" >> "$LOG"
  grep -n -i -E "verdict|FAILS|INERT|PASS" "$HERE/../CFG648_phase_mixed_settling/README.md" | head -12 >> "$LOG"
fi
while true; do
  N=$(ps -axo command= | awk '$1 ~ /python/ && $2 ~ /cfg(596|636|640|650)_pm[.]py$/' | wc -l | tr -d ' ')
  FI=$(vm_stat | awk '/page size of/{ps=$8}/Pages free/{f=$3}/Pages inactive/{i=$3}END{gsub("\\.","",f);gsub("\\.","",i);printf "%.1f",(f+i)*ps/1e9}')
  echo "$(date '+%Y-%m-%d %H:%M:%S') engine procs $N free+inactive ${FI} GB" >> "$LOG"
  if [ "$N" = "0" ] && awk -v x="$FI" -v n="$NEED_GB" 'BEGIN{exit !(x+0 >= n)}'; then
    cd "$HERE" || exit 1
    nohup nice -n 10 python3 "$RUNNER" serial "$JOB" > "$WORK/run_650_${JOB}_nohup.log" 2>&1 &
    echo "$(date '+%Y-%m-%d %H:%M:%S') LAUNCHED run_650.py serial $JOB (pid $!); waiter exits" >> "$LOG"
    exit 0
  fi
  sleep 120
done
