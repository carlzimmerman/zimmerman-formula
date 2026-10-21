#!/bin/bash
# CFG960 overnight chain (modelled on chain7b): the pre-registered 1024^3 SCT-M shear test (FROZEN_CRITERIA_1024.md).
#   SC1x (canonical) -> score MUTATE first -> score;  SC2x (alt) -> score MUTATE first -> score.  Control NCS0 (CFG654, existing).
# Heavy-job-only gate: waits while any heavy job runs (1024^3 engines: CFG6xx engines, CFG650/654 launchers, CFG596, CFG960's own
#   engine and launcher; an Ollama llama-server) and until free + inactive memory >= 46 GB and free disk >= 40 GB. Light single-core
#   lanes do not block the start (as chain7b). The frozen abort rule (RSS > 52 GB or swap growth > 4 GB) is enforced by run_960.py.
# Checkpoint / resume rule: the engine writes a rolling checkpoint (<tag>_ckpt in the job folder) after every step whose next force
#   call refreshes the census. If a job exits non-zero (abort rule, crash, reboot) and a checkpoint exists, the chain waits at the gate
#   again and restarts it, up to 3 restarts per job; the engine resumes bit-identically from the checkpoint. Finished steps leave
#   $ST/<step>.ok and are skipped when the chain is started again (e.g. after a reboot).
# Outputs are named by job: _external_data/cfg960_work/SC1x/, SC2x/ (engine), cfg960_score_results_SC1x[_MUTATE].json (lane folder).
# Start (the orchestrator, under the overnight gate, after review):  nohup bash chain960.sh > <EXT>/cfg960_work/chain960_nohup.log 2>&1 &
# kappa = 1/2 FITTED; footings never pooled; not theory closed.
HERE=$(cd "$(dirname "$0")" && pwd)
EXT=$(cd "$HERE/../../.." && pwd)/_external_data
W=$EXT/cfg960_work; ST=$W/chain960_state; LOG=$W/chain960.log; mkdir -p "$ST"
freegb () { vm_stat | awk '/page size of/{ps=$8}/Pages free/{f=$3}/Pages inactive/{i=$3}END{gsub("\\.","",f);gsub("\\.","",i);printf "%.0f",(f+i)*ps/1e9}'; }
diskgb () { df -g "$W" | awk 'NR==2{print $4}'; }
heavy () { pgrep -f "cfg6[0-9][0-9]_pm\.py|run_65[04]\.py|cfg596_pm|cfg960_sctm_pm\.py|run_960\.py|llama-server" >/dev/null; }
gate () { while heavy || [ "$(freegb)" -lt 46 ] || [ "$(diskgb)" -lt 40 ]; do sleep 60; done; }
step () {  # step NAME NEEDGATE RESTARTS JOBDIR CMD...
  local n=$1 g=$2 rmax=$3 jd=$4; shift 4
  [ -f "$ST/$n.ok" ] && { echo "$(date) chain960 $n already done (skip)" >> "$LOG"; return 0; }
  cd "$HERE" || exit 1
  local try=0 rc=1
  while :; do
    [ "$g" = 1 ] && gate
    echo "$(date) chain960 $n start (try $try; free $(freegb) GB; disk $(diskgb) GB)" >> "$LOG"
    eval "$@"; rc=$?
    echo "$(date) chain960 $n rc $rc" >> "$LOG"
    [ $rc -eq 0 ] && { touch "$ST/$n.ok"; return 0; }
    if [ -n "$jd" ] && ls -d "$W/$jd"/*_ckpt >/dev/null 2>&1 && [ $try -lt "$rmax" ]; then
      try=$((try + 1)); echo "$(date) chain960 $n: non-zero exit with a checkpoint present -> restart $try/$rmax after the gate (resume)" >> "$LOG"
    else
      echo "$(date) chain960 stopped after $n failure" >> "$LOG"; exit 1
    fi
  done
}
step SC1x 1 3 SC1x "nice -n 10 python3 run_960.py serial SC1x >> $W/run_960_SC1x_nohup.log 2>&1"
step scoreSC1x_mut 0 0 "" "OMP_NUM_THREADS=1 CFG596_MUTATE=1 nice -n 10 python3 cfg960_score.py --score SC1x > $W/score_SC1x_mut.log 2>&1"
step scoreSC1x 0 0 "" "OMP_NUM_THREADS=1 nice -n 10 python3 cfg960_score.py --score SC1x > $W/score_SC1x.log 2>&1"
step SC2x 1 3 SC2x "nice -n 10 python3 run_960.py serial SC2x >> $W/run_960_SC2x_nohup.log 2>&1"
step scoreSC2x_mut 0 0 "" "OMP_NUM_THREADS=1 CFG596_MUTATE=1 nice -n 10 python3 cfg960_score.py --score SC2x > $W/score_SC2x_mut.log 2>&1"
step scoreSC2x 0 0 "" "OMP_NUM_THREADS=1 nice -n 10 python3 cfg960_score.py --score SC2x > $W/score_SC2x.log 2>&1"
echo "$(date) chain960 done" >> "$LOG"
