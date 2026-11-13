#!/bin/bash
# AMENDMENT_A1: reading T runs after the frozen stages, as the same single job (waits on the frozen job's pid).
cd "$(dirname "$0")"
P=$1
while kill -0 "$P" 2>/dev/null; do sleep 30; done
nice -n 19 python3 frz3r_turn.py
touch run_turn.done
