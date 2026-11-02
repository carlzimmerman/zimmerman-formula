#!/bin/bash
# two chains, one thread each, nice 19, behind BF1 and UX7. compute_queue can't start this: BF1 over 4 GB footprint and disk under 30 GB block every start.
cd "$(dirname "$0")"; export AF1_NIT=400
(nice -n 19 python3 af1_stage3.py canonical; nice -n 19 python3 af1_stage3.py scrambled) > run_a.log 2>&1 &
(nice -n 19 python3 af1_stage3.py alt; nice -n 19 python3 af1_stage3.py planted) > run_b.log 2>&1 &
wait
