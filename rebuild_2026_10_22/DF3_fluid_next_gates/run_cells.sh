#!/bin/bash
# Lane queue: at most two processes, nice 19.
cd "$(dirname "$0")"
printf '%s\n' "law" "cell 1 100 N" "cell 5/3 100 N" "cell 1 30 N" "cell 5/3 30 N" "cell 2/3 30 N" "cell 1 100 S" "cell 5/3 100 S" "cell 1 30 S" "cell 5/3 30 S" "cell 2/3 30 S" | xargs -P 2 -I{} sh -c 'nice -n 19 python3 -I df3g_run.py {} > "run_$(echo {} | tr " /" "__").log" 2>&1'
echo done > cells.done.tmp
