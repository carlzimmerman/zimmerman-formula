#!/bin/sh
# usage: run_queue.sh JOBFILE NPAR     each line of JOBFILE: "<su2|su3> <point|wpoint> <L> <bF>"; NPAR jobs at a time (each wpoint job uses B4_WORKERS processes), nice 10, one log per job in logs/
JOBS=$1; NP=${2:-3}
cd "$(dirname "$0")" || exit 1
export B4_WORKERS=${B4_WORKERS:-3}
cat "$JOBS" | xargs -P "$NP" -L 1 sh -c 'g=$0; m=$1; L=$2; f=$3; script=b4_1_su2.py; [ "$g" = su3 ] && script=b4_2_su3.py; nice -n 10 python3 $script $m $L $f > logs/${g}_${m}_L${L}_bF${f}.log 2>&1'
