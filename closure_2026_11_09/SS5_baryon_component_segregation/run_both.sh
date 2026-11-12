#!/bin/bash
# SS5: both footings, one thread, nice 19 (a live box run shares the machine)
cd "$(dirname "$0")"
for f in canonical alt; do (time SS1_FOOT=$f nice -n 19 python3 ss5.py) > run_$f.txt 2>&1; done
