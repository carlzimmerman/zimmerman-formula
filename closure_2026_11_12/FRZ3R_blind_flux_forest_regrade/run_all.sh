#!/bin/bash
# FRZ3R: frozen stages in order (READING.md 7b). One job, nice 19, 4 threads. Restartable.
cd "$(dirname "$0")"
set -e
nice -n 19 python3 frz3r_run.py anchor 2.2 3.0 4.4
nice -n 19 python3 frz3r_run.py other 2.4 2.6 2.8 3.2 3.4 3.6 3.8 4.0 4.2
nice -n 19 python3 frz3r_run.py res 2.2 3.0 4.4
nice -n 19 python3 frz3r_run.py clustered 2.2 3.0 4.4
touch run_all.done
