#!/bin/bash
# SRF1: one job, stages in order (AMENDMENT_A1 item 7). nice 19, 4 threads in all. Restartable (parts are skipped).
cd "$(dirname "$0")"
export SRF1_THREADS=2
set -e

nice -n 19 python3 srf1_tables.py 2.2 3.0 4.4 2.4 2.6 2.8 3.2 3.4 3.6 3.8 4.0 4.2
nice -n 19 python3 srf1_run.py primary 2.2 3.0 4.4
nice -n 19 python3 srf1_run.py primary 2.4 2.6 2.8 3.2 3.4 3.6 3.8 4.0 4.2
nice -n 19 python3 srf1_run.py bracket 2.2 3.0
nice -n 19 python3 srf1_run.py clustered 2.2
nice -n 19 python3 srf1_run.py res 2.2
touch run_all.done
