#!/bin/bash
# Run the profiler wrapper, dumping stacks at 20/40/55 s via SIGUSR1.
cd "$(dirname "$0")"
python3 run_wrapper_prof.py > raw_output.json 2> raw_output.stderr &
WPID=$!
sleep 20; kill -USR1 $WPID 2>/dev/null
sleep 20; kill -USR1 $WPID 2>/dev/null
sleep 15; kill -USR1 $WPID 2>/dev/null
wait $WPID
echo "exit=$?"
